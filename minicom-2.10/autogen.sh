#! /bin/sh
#
# $Id: autogen.sh,v 1.16 2009-11-15 20:00:56 al-guest Exp $

AUTOMAKEVER=1.16

set -x

aclocal-$AUTOMAKEVER
[ "$?" != 0 ] && echo "aclocal-$AUTOMAKEVER not available or failed!" && exit 1
autoheader || exit 1
automake-$AUTOMAKEVER -c --add-missing --force --gnu || exit 1
autoconf || exit 1

# remove once it comes via config.sub directly
perl -p -i -e 's/(\| hcos\* )/$1| l4re* /' config.sub
