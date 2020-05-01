# Testing Framework for OS 234123 - HW 1
## Created by Ronen Sandler and Amitai Frey

### Important

Please do not immediately contact us if the framework/tests don't work for
 you. They have been verified by multiple students and therefore are
  probably accurate.
  
Nevertheless, if you are convinced you have found a bug please explain
 exactly what the bug is and **provide an exact section in the
  assignment / piazza post that proves you are correct. Otherwise, we
   will simply not answer your questions.** 
   
This is done in order to help us from solving bugs for everyone, so
 we can apply our time to fix the actual bugs we might still have and to
  benefit the rest of the class.

### Requirements
* Smash executable
* The attached generated tests
* Python 3
* Ability & maturity to debug code yourself

### Basic Usage
1. Copy the tests framework folder to your machine, with the tests
2. In that folder, run: `./test.py -smash="<your_smash>" -test="unit"`
3. Check the output for diffs/equal prompts

### Advanced Usage
* In order to run a specific test by its name, run: `./test.py -smash
="<your_smash>" -test="<test_name>"`. For example: `./test.py -smash
="smash" -test="unit/jobs"`
* In order to generate tests of your own, create a test.in and test.exp
 files, where the test.exp file matches by regex the expected output
  line by line.
* Additionaly, you may specify a (flat) directory of your choice containing `.in` and `.exp` files in the with the command `./test.py -smash="<your_smash>" -test="<directory_path>"`


  
### Details

* This framework utilizes difflib's SequenceMatcher, but enhances it by
 comparing each line by regex. This helps us test on different machines
  with different pids without having to "hack" them to get what we want
  . These regexs include:
  * `\d+` for pids and secs numbers
  * `\[`, `\]`, `\(`, `\)` for escaping these chars so the regex matches
   them plainly.
  * Of course the framework supports standard regex matching. The sky is
   the limit! 
* Additionally, the framework supports comparing regex groups in
 multiple lines. This can help make sure you get the same output in
  different calls by the same test. For example, in order to make sure
   that the pid stays the same, you can write: `smash> smash pid is (?P
   <pid>\d+)` in the *.exp file every time you run `showpid`. The
    framework will make sure that the regex group `pid` always has the
     same value.  
* This framework also relies on setting up the /tmp/smash_test directory 
 as we expect it, with random files for copying and checking.
* You can comment the input files by starting the line with `#`
* You can add lines to the input file that will be run in the python
 framework directly by starting them with `!`, for ex: `!time.sleep(2)` will cause the framework to sleep for 2 seconds.
* In order to send Ctrl-C or Ctrl-Z signals, simply write in a separate
 line in the input file `CtrlC` or `CtrlZ` respectively.
* Also added to the framework is my_sleep.c, which is compiled during
 setup and copied to the test dir. It is run by: `my_sleep <n>` where n
  is the number of seconds it will sleep, printing the time that has
   passed every two seconds. 
* The tests that are contained in this repository consist of unit
 tests written for common edge-cases. If you have additional test cases that are not checked here, please open a
  pull request for us with them and we will be happy to add them to the
   repository.
