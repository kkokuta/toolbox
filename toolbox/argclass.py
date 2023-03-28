from argparse import ArgumentParser
from typing import Literal


def argclass(cls):
    parser = ArgumentParser()
    arg2default = {arg: default for arg, default in cls.__dict__.items() if not arg.startswith("__")}
    arg2type = cls.__annotations__

    for arg, type_ in arg2type.items(): 
        arg_str = "--" + arg.replace("_", "-")
        kwargs = dict()
        nargs = 1

        if type(type_) is not type:
            # e.g., beta: list[str, str], option: Literal["A", "B", "C"], ...
            args = type_.__args__
            assert len({type(arg) for arg in args}) == 1, "type arguments should be explicit and all should be the same."
            arg_type = type(args[0])
            if arg_type is type:
                # e.g., beta: list[str, str]
                assert len(set(args)) == 1, "the classes for nargs should be all the same."
                type_ = args[0]     # => str
                nargs = len(args)
                kwargs["nargs"] = nargs
            else:
                # e.g., option: Literal["A", "B", "C"]
                type_ = arg_type    # => str
                kwargs["choices"] = args        # => ('A', 'B', 'C')
        
        if type_ is bool:
            # e.g., skip_test: bool
            kwargs["action"] = "store_true"
            if arg in arg2default:
                default = arg2default[arg]
                kwargs["action"] = "store_false" if default else "store_true"
        else:
            # e.g., n_epochs: int, beta: list[str, str], option: Literal["A", "B", "C"], ...
            kwargs["type"] = type_
            if arg in arg2default:
                default = arg2default[arg]
                if "choices" in kwargs:
                    assert default in kwargs["choices"], f"the default value is invalid. {default!r} is not an option."
                kwargs["default"] = default

        parser.add_argument(arg_str, **kwargs)

    return parser.parse_args()


def sample_use():
    from typing import Tuple

    @argclass
    class Args:
        n_epoch: int = 100
        model: Literal["bert", "roberta", "albert"] = "bert"
        output_dir: str
        device: str = "cuda:0"
        use_cpu: bool
        beta: tuple[float, float] = (0.2, 0.4)

    Args.output_dir = Args.output_dir.rstrip("/")

    print(Args.n_epoch)
    print(Args.model)
    print(Args.output_dir)
    print(Args.device)
    print(Args.use_cpu)
    print(Args.beta)


if __name__ == "__main__":
    sample_use()