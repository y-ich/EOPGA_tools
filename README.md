# Analysis Tools for "ELF OpenGo Professional Game Analysis"

## About "ELF OpenGo Professional Game Analysis"

See [ELF OpenGo](https://ai.facebook.com/tools/elf-opengo).

## Target

The target of the tools is [SGF files which were analyzed with ELF OpenGo](https://dl.fbaipublicfiles.com/elfopengo/analysis/data/gogod_commentary_sgfs.gzip).

## Tools

### winrates.py

calculates winrate transition of each SGF.

```sh
python winrates.py <gogod folder> > winrates.raw.csv
```

### check_variations.py

outputs SGFs with the illegal main line or variation.
If you want to check only main line, use check_main_line.py.

```sh
python check_variations.py <gogod folder> > illegal_variation_sgfs.txt
```

### filter_by_list_file.py

filters lines with any of word list file.

```sh
python filter_by_list_file.py winrates.raw.csv illegal_variation_sgfs.txt > winrates.csv
```

### delta_winrates.py

outputs the positions with AI's wonderful suggestions and professionals' execellent play moves.

## License

MIT