import argparse

from cognitive_graph.datasets import DATASET_REGISTRY
from cognitive_graph.models import MODEL_REGISTRY
from cognitive_graph.tasks import TASK_REGISTRY


def get_parser():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    # fmt: off
    # parser.add_argument('--log-interval', type=int, default=1000, metavar='N',
    #                     help='log progress every N batches (when progress bar is disabled)')
    # parser.add_argument('--tensorboard-logdir', metavar='DIR', default='',
    #                     help='path to save logs for tensorboard, should match --logdir '
    #                          'of running tensorboard (default: no tensorboard logging)')
    parser.add_argument('--seed', default=1, type=int, nargs='+', metavar='N',
                        help='pseudo random number generator seed')
    parser.add_argument('--max-epoch', default=1000, type=int)
    parser.add_argument("--patience", type=int, default=100)
    parser.add_argument('--lr', default=0.005, type=float)
    parser.add_argument('--weight-decay', default=5e-4, type=float)
    parser.add_argument('--cpu', action='store_true', help='use CPU instead of CUDA')
    parser.add_argument('--device-id', default=0, type=int,
                       help='which GPU to use')
    parser.add_argument('--save-dir', default='.', type=str)
    # fmt: on
    return parser


def add_task_args(parser):
    group = parser.add_argument_group("Task configuration")
    # fmt: off
    group.add_argument('--task', '-t', default='node_classification', metavar='TASK', required=True,
                       choices=TASK_REGISTRY.keys(),
                       help='Task')
    # fmt: on
    return group


def add_dataset_args(parser):
    group = parser.add_argument_group("Dataset and data loading")
    # fmt: off
    group.add_argument('--dataset', '-dt', metavar='DATASET', nargs='+', required=True,
                       choices=DATASET_REGISTRY.keys(),
                       help='Dataset')
    # fmt: on
    return group


def add_model_args(parser):
    group = parser.add_argument_group("Model configuration")
    # fmt: off
    group.add_argument('--model', '-m', default='gcn', metavar='MODEL', nargs='+', required=True,
                       choices=MODEL_REGISTRY.keys(),
                       help='Model Architecture')
    # fmt: on
    return group


def get_training_parser():
    parser = get_parser()
    add_task_args(parser)
    add_dataset_args(parser)
    add_model_args(parser)
    return parser


def get_display_data_parser():
    parser = get_parser()
    add_dataset_args(parser)
    parser.add_argument("--depth", default=3, type=int)

    return parser


def parse_args_and_arch(parser, args):
    """The parser doesn't know about model-specific args, so we parse twice."""
    # args, _ = parser.parse_known_args()

    # Add model-specific args to parser.
    model_specific_group = parser.add_argument_group(
        "Model-specific configuration",
        # Only include attributes which are explicitly given as command-line
        # arguments or which have default values.
        argument_default=argparse.SUPPRESS,
    )
    MODEL_REGISTRY[args.model].add_args(model_specific_group)

    # Add *-specific args to parser.
    TASK_REGISTRY[args.task].add_args(parser)

    # Parse a second time.
    args = parser.parse_args()

    return args
