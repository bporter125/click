# -*- coding: utf-8 -*-
import re
import click


def test_other_command_invoke(runner):
    @click.command()
    @click.pass_context
    def cli(ctx):
        return ctx.invoke(other_cmd, 42)

    @click.command()
    @click.argument('arg', type=click.INT)
    def other_cmd(arg):
        click.echo(arg)

    result = runner.invoke(cli, [])
    assert not result.exception
    assert result.output == '42\n'


def test_other_command_forward(runner):
    cli = click.Group()

    @cli.command()
    @click.option('--count', default=1)
    def test(count):
        click.echo('Count: %d' % count)

    @cli.command()
    @click.option('--count', default=1)
    @click.pass_context
    def dist(ctx, count):
        ctx.forward(test)
        ctx.invoke(test, count=42)

    result = runner.invoke(cli, ['dist'])
    assert not result.exception
    assert result.output == 'Count: 1\nCount: 42\n'


def test_auto_shorthelp(runner):
    @click.group()
    def cli():
        pass

    @cli.command()
    def short():
        """This is a short text."""

    @cli.command()
    def long():
        """This is a long text that is too long to show as short help
        and will be truncated instead."""

    result = runner.invoke(cli, ['--help'])
    assert re.search(
        r'Commands:\n\s+'
        r'long\s+This is a long text that is too long to show\.\.\.\n\s+'
        r'short\s+This is a short text\.', result.output) is not None


def test_default_maps(runner):
    @click.group()
    def cli():
        pass

    @cli.command()
    @click.option('--name', default='normal')
    def foo(name):
        click.echo(name)

    result = runner.invoke(cli, ['foo'], default_map={
        'foo': {'name': 'changed'}
    })

    assert not result.exception
    assert result.output == 'changed\n'
