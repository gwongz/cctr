# cctr
Playing around with John Crickett's Coding Challenge to [write your own tr tool](https://codingchallenges.fyi/challenges/challenge-tr).

### Getting Started

#### Requirements
In order to run cctr you will need to have [Python ^3.10](https://www.python.org/downloads/) installed.


* Clone the repo:
    ```
    git clone https://github.com/gwongz/cctr.git
    ```

* Install the dev requirements (only if you want to run tests)

    ```
    pip install -r requirements_dev.txt
    ```

* Run end-to-end tests.
    ```
    pytest
    ```

### Usage
Use `cctr` just as you would the `tr` command.

See `man tr` for options. (Note: squeeze is not implemented in this version and not all class specifiers are implemented).

Use the `test.txt` file if you need a sample text file.

### Examples


```
# translate lowercase h to uppercase H
% cctr h H
hello, world!
Hello, world!

# translate uppercase to lowercase
% head -n1 test.txt | cctr "[:upper:]" "[:lower:]"
the project gutenberg ebook of the art of war

# translate hijk to rstu
% echo hello | cctr h-k r-u
uello

# delete all l characters from the input
% echo Hello, World! | cctr -d l
Heo, Word!
```

