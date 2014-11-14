all: create-virenv launch-ipython-notebook

create-virenv:

	# pip is needed for installing some python packages
	conda create --yes -n comm-health ipython-notebook=2.0 \
		pip matplotlib pandas xlrd

	source activate comm-health

launch-ipython-notebook:

	ipython notebook --pylab inline
