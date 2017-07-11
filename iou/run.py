#!/usr/bin/env python
"""Run module."""

import click
from . import data
from . import version
from . import ReferenceModel

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--data', type=click.Path(), help='Path to transactions.csv')
@click.option('--verbose', default=False, is_flag=True, help='Verbose mode')
@click.option('--color', default='green', help='Color of text')
@click.option('--verbose-color', default='white', help='Color of text')
@click.version_option(version.__version__, '-v', '--version')
def main(**kwargs):
    """iou - Find optimal transactions."""

    color = kwargs['color']

    try:
        if not any([kwargs[key] for key in ['data']]):
            help_str = "{}".format(click.get_current_context().get_help())
            click.secho(help_str)
            click.get_current_context().exit()

        def show_item(item):
            if item is not None:
                return item

        click.echo("")
        click.secho("Find the Optimal Number of Transactions:", fg=color, bold=True)
        click.echo("")

        with click.progressbar(
            ('Getting data', 'Creating model', 'Solving', 'Finished'),
                label='iou:',
                item_show_func=show_item) as bar:
            for item in bar:
                if item == 'Getting data':
                    path_to_file = kwargs['data']
                    array, people = data.get_transactions_from_file(path_to_file)
                    net_value = data.compress_edges(data.create_graph(array, people))
                elif item == 'Creating model':
                    model = ReferenceModel.create_model(net_value)
                elif item == 'Solving':
                    ReferenceModel.solve(model)

        if kwargs['verbose']:
            color = kwargs['verbose_color']
            click.echo("")
            for row_number, row in enumerate(array):
                number_of_contributors = sum([float(item) for item in row[3:]])

                click.secho("{number_of_contributors}".format(number_of_contributors=number_of_contributors), bold=True, fg=color, nl=False)
                click.secho(" people owe ", nl=False)
                click.secho("{person}".format(person=row[2]), bold=True, fg=color, nl=False)
                click.secho(" ", nl=False)
                click.secho("{amount}".format(amount=row[1]), bold=True, fg=color, nl=False)
                click.secho(" for ", nl=False)
                click.secho("{expense}".format(expense=row[0]), bold=True, fg=color)

            click.echo("")
            for person, value in net_value.items():
                if value > 0:
                    click.secho("{person}".format(
                        person=person), bold=True, fg=color, nl=False)
                    click.secho("'s net spend =", nl=False)
                    click.secho(" {value}".format(value=value), bold=True, fg=color)

            click.echo("")
            for person, value in net_value.items():
                if value < 0:
                    click.secho("{person}".format(
                        person=person), bold=True, fg=color, nl=False)
                    click.secho("'s net spend =", nl=False)
                    click.secho(" {value}".format(value=value), bold=True, fg=color)

        click.echo("")

        color = kwargs['color']

        click.secho("iou results:")

        click.echo("")

        for i in model.Amount:
            if model.Amount[i].value == 0:
                pass
            else:
                click.secho("{}".format(i[0]), fg=color, bold=True, nl=False)
                click.secho(" owes", nl=False)
                click.secho(" {}".format(i[1]), fg=color, bold=True, nl=False)
                click.secho(" a total of ", nl=False)
                click.secho("${0:.2f}".format(model.Amount[i].value), fg=color, bold=True)

        click.echo("")

    except Exception as e:
        click.echo('')
        raise click.ClickException("{}\n\nCheck the help (--help) on how to use iou or contact the developer.".format(
            e.message))


if __name__ == '__main__':
    main()
