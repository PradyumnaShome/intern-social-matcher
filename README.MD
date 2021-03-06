# Intern Social Matcher
Get introduced to new employees at your workplace, every week.

Hosted [here](https://pradyumnashome.github.io/intern-social-matcher/) using GitHub Pages!

I used Google Forms -> CSV to get data from my fellow interns.
[Here](https://github.com/PradyumnaShome/intern-social-matcher/blob/master/interns_with_interests.csv) is a sample input intern file with the fields I collected. 

## Usage

### Generate Matches

Run `make generate`.

To generate matches, run

```bash
    python3 intern_social_matcher.py <intern_list_file> <group_size>
```

where

`intern_list_file` is a file with a list of interns, delimited by newlines.

`group_size` is the number of people you'd like to meet every time

### Render intern matching output

Run `make render`.

To render a web page, run

```bash
    python3 render_matches.py <matches_file> <output_file>
```

where

`matches_file` is a file with the output from the first step. It has generated matches in a double-nested JSON list.

`output_file` is the HTML file that is rendered from the matches.

To do both in sequence, run `make all`.