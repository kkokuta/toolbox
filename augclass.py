from argparse import ArgumentParser
from collections.abc import Iterable


def argclass(cls):
    parser = ArgumentParser()
    arg2default = {arg: default for arg, default in cls.__dict__.items() if not arg.startswith("__")}
    arg2type = cls.__annotations__

    for arg, type_ in arg2type.items():
        arg_str = "--" + arg.replace("_", "-")
        kwargs = dict()
        nargs = 1

        if type(type_) is not type:
            types = type_.__args__
            assert len(set(types)) == 1, "the classes for nargs should be all the same."
            type_ = types[0]
            nargs = len(types)
            kwargs["nargs"] = nargs

        if type_ is bool:
            kwargs["action"] = "store_true"
            if arg in arg2default:
                default = arg2default[arg]
                kwargs["action"] = "store_false" if default else "store_true"
        else:
            kwargs["type"] = type_
            if arg in arg2default:
                default = arg2default[arg]
                if isinstance(default, Iterable) and not isinstance(default, str) and nargs == 1:
                    kwargs["choices"] = default
                    if hasattr(default, "__getitem__"):
                        kwargs["default"] = default[0]
                else:
                    kwargs["default"] = default

        parser.add_argument(arg_str, **kwargs)

    return parser.parse_args()


def sample_use():
    from typing import Tuple
    
    @argclass
    class Args:
        n_epoch: int = 100
        model: str = ["bert", "roberta", "albert"]      # the first element is the default value if it is subscriptable
        output_dir: str
        device: str = "cuda:0"
        use_cpu: bool
        beta: Tuple[float, float] = (0.2, 0.4)

    Args.output_dir = Args.output_dir.rstrip("/")

    print(Args.n_epoch)
    print(Args.model)
    print(Args.output_dir)
    print(Args.device)
    print(Args.use_cpu)
    print(Args.beta)


if __name__ == "__main__":
    sample_use()