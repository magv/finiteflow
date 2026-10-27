CC=cc
CXX=c++
FETCH=python3 bin/urlget

UNAME_S:=$(shell uname -s)

ifeq ($(UNAME_S),Darwin)
SHA256_CHECK=shasum -a 256 -c -
GC_SECTIONS_LDFLAG=-Wl,-dead_strip
else
SHA256_CHECK=sha256sum -c -
GC_SECTIONS_LDFLAG=-Wl,--gc-sections
endif

DIR=${CURDIR}
DEP_CFLAGS=-I${DIR}/include -O3 -fPIC -fno-omit-frame-pointer -fdata-sections -ffunction-sections ${CFLAGS}
DEP_LDFLAGS=-L${DIR}/lib ${GC_SECTIONS_LDFLAG} ${LDFLAGS}

MAKEOVERRIDES =

build/.dir:
	mkdir -p bin build include lib share
	echo "import sys; from urllib.request import urlretrieve as get; get(sys.argv[2], filename=sys.argv[1])" >bin/urlget
	date >$@

clean: phony
	rm -rf bin/ build/ include/ lib/ share/ *.done

phony:;

## GMP

VER_gmp=6.3.0
SHA256_gmp=a3c2b80201b89e68616f4ad30bc66aee4927c3ce50e33929ca819d5c43538898

build/gmp-${VER_gmp}.tar.xz: build/.dir
	rm -f build/gmp*.tar.xz
	${FETCH} $@ "https://ftpmirror.gnu.org/gmp/gmp-${VER_gmp}.tar.xz" \
		|| ${FETCH} $@ "https://ftp.gnu.org/gnu/gmp/gmp-${VER_gmp}.tar.xz" \
		|| ${FETCH} $@ "https://gmplib.org/download/gmp/gmp-${VER_gmp}.tar.xz" \
		|| { rm -f $@; exit 1; }
	{ echo "${SHA256_gmp}  $@" | ${SHA256_CHECK}; } || { rm -f $@; exit 1; }

gmp.done: build/gmp-${VER_gmp}.tar.xz
	rm -rf build/gmp-*/
	cd build && tar xf gmp-${VER_gmp}.tar.xz
	cd build/gmp-*/ && mv configfsf.guess config.guess
	cd build/gmp-*/ && \
		env CC="${CC}" CXX="${CXX}" CFLAGS="-std=c11 ${DEP_CFLAGS}" CXXFLAGS="${DEP_CFLAGS}" LDFLAGS="${DEP_LDFLAGS}" \
		./configure \
		--prefix="${DIR}" --libdir="${DIR}/lib" \
		--includedir="${DIR}/include" --bindir="${DIR}/bin" \
		--enable-static --disable-shared --enable-cxx --with-pic --enable-assembly=no
	+${MAKE} -C build/gmp-*/
	+${MAKE} -C build/gmp-*/ install
	date >$@

## flint-finiteflow

VER_flint-finiteflow=3f2380a7d3daa73876d4d8e71fe908b7a82cb914
SHA256_flint-finiteflow=31bfa6c121c81d63b237b1d7ba6019880054772334e1835edd21418472ed2aeb

build/flint-finiteflow-dep-${VER_flint-finiteflow}.tar.gz: build/.dir
	rm -f build/flint-finiteflow-dep-*.tar.gz
	${FETCH} $@ "https://github.com/peraro/flint-finiteflow-dep/archive/${VER_flint-finiteflow}.tar.gz" \
		|| { rm -f $@; exit 1; }
	{ echo "${SHA256_flint-finiteflow}  $@" | ${SHA256_CHECK}; } || { rm -f $@; exit 1; }

build/flint-finiteflow-dep-${VER_flint-finiteflow}/.dir: build/flint-finiteflow-dep-${VER_flint-finiteflow}.tar.gz
	rm -rf build/flint-finiteflow-dep-*/
	cd build && tar xf flint-finiteflow-dep-${VER_flint-finiteflow}.tar.gz
	touch build/flint-finiteflow-dep-${VER_flint-finiteflow}/.dir

FLINT_FINITEFLOW_SRCDIR=build/flint-finiteflow-dep-${VER_flint-finiteflow}
FLINT_FINITEFLOW_OBJ=${addprefix ${FLINT_FINITEFLOW_SRCDIR}/, \
	generic_files/clz_tab.o \
	ulong_extras/dummy.o \
	ulong_extras/gcdinv.o \
	ulong_extras/gcd.o \
	ulong_extras/ll_mod_preinv.o \
	ulong_extras/mod2_preinv.o \
	ulong_extras/mulmod_preinv.o \
	ulong_extras/powmod2_ui_preinv.o}

${FLINT_FINITEFLOW_SRCDIR}/%.o: ${FLINT_FINITEFLOW_SRCDIR}/.dir
	cd ${FLINT_FINITEFLOW_SRCDIR} && ${CC} ${DEP_CFLAGS} -std=c11 -I. -c $*.c -o $*.o

flint-finiteflow.done: ${FLINT_FINITEFLOW_OBJ} gmp.done
	ar rcs lib/libflint.a ${FLINT_FINITEFLOW_OBJ}
	mkdir -p include/flint
	cp ${FLINT_FINITEFLOW_SRCDIR}/*.h include/flint/
	date >$@
