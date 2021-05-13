The rNSP package contains some basic codes for manipulating NSP data and plotting maps and networks. To use it, you will need to install the package.

To install, either open R to the rNSP directory, or open RStudio and set the working directory to the rNSP directory. First, we need to install the devtools, if not already installed. In the console, type the following:

    install.packages("devtools")

On a mac, the installation may require

    brew install libgit2

for `git2r` dependency. Next, load the devtools library

    library("devtools")

Now that the devtools library is installed and we are in the rNSP directory, we can build the package

    build()

And now finally, we can install it

    install()

Now, you should be able to load the rNSP package into any file in your local machine by calling:

    library("rNSP")

A thorough explanation of installing R packages can be found at the following link: [kbroman.org/pkg_primer/pages/build.html](kbroman.org/pkg_primer/pages/build.html)
