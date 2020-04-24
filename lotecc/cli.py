"""Console script for lotecc."""
import sys
import click

from lotecc.lotecc import lote_chinese_conversion


@click.command()
@click.option('-c', '--conversion', 'conversion', default='s2t', show_default=True,
              help='Conversion method between Simplified Chinese and Traditional Chinese.')
@click.option('-i', '--input', 'input_', default='.',
              help='Input file or directory. The default is current dir.')
@click.option('-o', '--output', 'output', default=None,
              help='Output file or directory. The default is the same as the source file, '
                   'which means that the source file will be overwritten.')
@click.option('--ignore', 'ignore', default='.gitignore', show_default=True,
              help='Can be a .gitignore syntax file. Also can be one or more patterns, separated by commas.')
@click.option('--suffix', 'suffix', default=None, show_default=False,
              help='Suffix of output filename, add this to keep both the source file and converted file.')
@click.option('--in-enc', 'in_enc', default='UTF-8', show_default=True, help='Encoding for input.')
@click.option('--out-enc', 'out_enc', default='UTF-8', show_default=True, help='Encoding for output.')
def main(**kwargs):
    """Convert files between Simplified Chinese and Traditional Chinese.

    Supported conversions:

        hk2s: Traditional Chinese (Hong Kong standard) to Simplified Chinese\n
        s2hk: Simplified Chinese to Traditional Chinese (Hong Kong standard)\n
        s2t: Simplified Chinese to Traditional Chinese\n
        s2tw: Simplified Chinese to Traditional Chinese (Taiwan standard)\n
        s2twp: Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)\n
        t2hk: Traditional Chinese to Traditional Chinese (Hong Kong standard)\n
        t2s: Traditional Chinese to Simplified Chinese\n
        t2tw: Traditional Chinese to Traditional Chinese (Taiwan standard)\n
        tw2s: Traditional Chinese (Taiwan standard) to Simplified Chinese\n
        tw2sp: Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)\n
    """

    try:
        lote_chinese_conversion(**kwargs)
    except Exception as e:
        click.echo(e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
