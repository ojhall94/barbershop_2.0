# barbershop

barbershop is a Python module that aids the user in making dynamic cuts to data in various parameter spaces & investigate said data spaces, using a simple GUI.

NOTE: API documentation for this package is not available yet (working on it!). The example enclosed
in this repo goes through the full functionality step by step though, so please use that in the mean time.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. barbershop now functions in both Python 2.x and 3.x.

### Installing

To install barbershop on your local UNIX machine, you can install it from commandline using pip:

```
sudo pip install barbershop
```

or if you don't have root privileges on your system:

```
pip install barbershop --user
```

For installations to Python3, please use

```
pip3
python3
```

instead of pip and python in the commands respectively.

If you enjoy hacking or want to contribute to barbershop, feel free to clone the Git repository and branch off to make your own changes.
In a directory of your choice, run the following from commandline:

```
git clone https://github.com/ojhall94/barbershop.git
cd barbershop
git branch <your-branch-name>
git checkout <your-branch-name>
sudo python setup.py install
```
The final line can be used to install any changes you make to your local repository to your local machine.
If you are new to GitHub, this 'cheat-sheet' might help with commandline commands: https://www.git-tower.com/blog/git-cheat-sheet/

## Running and example

barbershop comes with a simple testing example, and some TRILEGAL (Girardi et al. 2012) data to run it with.
The file can be found in the Git repo for this package, which can be cloned to your local machine in a directory of choice.


```
git clone https://github.com/ojhall94/barbershop.git
cd barbershop/example/
python test_barbershop.py
```

I highly recommend you open test_barbershop.py in your editor of choice and read through it.
I've provided comments for each step and it outlines the full functionality of the package.

If you encounter any issues with running this program as described above, please email me with the
exact issues you encountered and steps to reproduce the bugs.


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Oliver James Hall** - Email: ojhall94@gmail.com | [Github](https://github.com/ojhall94) | [Twitter](https://www.twitter.com/ojhall94)

If you have any questions about the package or wish to contribute, please drop me a message on any of the above platforms.

## License

Copyright 2018 Oliver James Hall and contributors.

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to anyone who bounced fun function names off me!
* Special thanks to all the mysterious people that answer StackOverflow questions.
* All credit for the barbershop quartet easter-egg idea goes to Matt Heath.
