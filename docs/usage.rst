=====
Usage
=====

To use ``lotecc`` in terminal::

    $ lotecc

Above command is equal to ``$ lotecc -c s2t -i . --ignore .gitignore``. Which convert all files in current directory and subdirectories from Simplified Chinese to Traditional Chinese, excluding files matching the pattern in ``.gitignore``:

- ``-c s2t``: conversion is Simplified Chinese to Traditional Chinese
- ``-i .``: input is current directory
- ``--ignore .gitignore``: files excluding files matching the pattern in ``.gitignore``

To use ``lotecc`` in a project::

    from lotecc import lote_chinese_conversion as lotecc

    lotecc(conversion='s2t',
           input='.',
           output=None,
           in_enc='utf-8',
           out_enc='utf-8',
           suffix=None,
           ignore='.gitignore')

You can get helps by type ``$ lotecc --help`` in terminal::

    Options:
      -c, --conversion TEXT  Conversion method between Simplified Chinese and
                             Traditional Chinese.  [default: s2t]
      -i, --input TEXT       Input file or directory. The default is current dir.
      -o, --output TEXT      Output file or directory. The default is the same as
                             the source file, which means that the source file
                             will be overwritten.
      -q, --quiet            Disable screen output.  [default: False]
      --ignore TEXT          Can be a .gitignore syntax file. Also can be one or
                             more patterns, separated by commas.  [default:
                             .gitignore]
      --suffix TEXT          Suffix of output filename, add this to keep both the
                             source file and converted file.
      --in-enc TEXT          Encoding for input.  [default: utf-8]
      --out-enc TEXT         Encoding for output.  [default: utf-8]
      --help                 Show this message and exit.

Supported conversions
=====================

- ``hk2s``: Traditional Chinese (Hong Kong standard) to Simplified Chinese\n
- ``s2hk``: Simplified Chinese to Traditional Chinese (Hong Kong standard)\n
- ``s2t``: Simplified Chinese to Traditional Chinese\n
- ``s2tw``: Simplified Chinese to Traditional Chinese (Taiwan standard)\n
- ``s2twp``: Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)\n
- ``t2hk``: Traditional Chinese to Traditional Chinese (Hong Kong standard)\n
- ``t2s``: Traditional Chinese to Simplified Chinese\n
- ``t2tw``: Traditional Chinese to Traditional Chinese (Taiwan standard)\n
- ``tw2s``: Traditional Chinese (Taiwan standard) to Simplified Chinese\n
- ``tw2sp``: Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)\n
