create-virenv:

	# pip is needed for installing some python packages
	conda create --yes -n comm-health ipython-notebook=2.0 \
		pip matplotlib=1.4.2 pandas=0.15.1 xlrd=0.9.2; \

launch-ipnb:

	ipython notebook --pylab inline

remove-env:

	conda remove --yes -n comm-health --all
