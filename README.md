### Author: Sofia Chelpon 07/27/2020

### TTS Read Me 
### All info regarding TTS work in this repository 
### Summary and instructions on how to use what is inside each directory 
### General notes needed to know to run 

________________________________________________________________________________
## What you will find in each directory: 

##### base_tts_code
This is most important for you, this contains almost everything you should need to do the fits 

	fitting.ipynb
		- start to finish process for using ratio data and lifetimes to fit a mu*-tau relationship 
		- note you want the lifetimes/ratios to be in ascending order arranged by lifetime & remove all nan 
		- fit relies on iteratively finding the minimum MSE and stopping when the MSE stops improving 
		- shows code for plotting mu*-tau best fit and G(t) 

	tts_mod.py
		- this is a module that packages together all the tts functions used 
		- essentially makes what I do in fitting.ipynb callable 
		- prep_for_tts —> feed it your lifetimes in ascending order, and it will return the timescale for G(t), the exponential decay matrix needed to get the G(t), and lifetimes in seconds 
		- my_greens_func —> solve analytical solution for Greens Function for a given K
		- get_tts —> iteratively test K values to find the minimum MSE fit for a set of ratios and lifetimes 
		- plot_tts —> produces plots when given all info about ratios, mu*, tau, G(t), etc… can toggle what information you want to show or not show with inputs (e.g. add_meanmode = 1 prints mean and mode on figure, = 0 does not) 

	  /testing 
		- code development, ignore this 

##### contrast_readin
This is how the CONTRAST data is read in. Direct to whatever directory you have desired CONTRAST files in. ONLY have files you want to read in in that directory, as xarray’s open_mfdataset will read in everything in the folder. I move flights I do not want to read in (eg transit flights RF01, 02, 16) to a different folder. 

	  awas 
		awas_readin_UTC.ipynb
			- read in all awas data from desired flights 
			- choose selected trace gases 
			- confine to study area (0-25 N) 
			- save 2 versions - one with and one without <LOD correction (fill values to ~1/2 estimated LOD) 
			- add species lifetimes 
			- remove all data immediately surrounding Guam 
			- add info on each flight & parameters (eg altitude, latitude, UTC time …) 
			- save to netcdf 
	  toga_lodhalf 
		ignore subdirectories, for development 
		toga_readin_lodhalf_noguam_UTC.ipynb
			- read in all awas data from desired flights 
			- choose selected trace gases 
			- confine to study area (0-25 N) 
			- do <LOD correction and fill values to ~1/2 estimated LOD 
			- add species lifetimes from xlsx file 
			- remove all data immediately surrounding Guam 
			- add info on each flight & parameters (eg altitude, latitude, …) 
			- save to netcdf 
		examine_flight_times.ipynb
			- get info on flight start/stop times so we can label each data point with an RF later 
		get_ut_flight_speed_temp.ipynb 
			- get info on avg UT temperature and speed 
			- to estimate length of UT sample and get UT temperature for calculating lifetimes 
	
##### get_ratios
This takes the read in TOGA and AWAS data and adds relevant information to each data point (RF, some metadata for each flight). Data is partitioned into UT and BL for the whole campaign and for each RF individually and ratios are calculated. Species lifetime is added for each trace gas. Data is merged into one “master list” where TOGA and AWAS are now stored in the same dataframe. 

There are several versions of the same code from different iterations/data treatments. First you want to run a version of DATA_PREP…, then that output gets read into GET_RATIOS… 

	data_prep.ipynb
			- uses UTC to tag each data point with the corresponding RF and add some metadata 
			- toga and awas done separately 
			- awas version WITHOUT <LOD correction 

	data_prep_awas_fills.ipynb
			- uses UTC to tag each data point with the corresponding RF and add some metadata 
			- toga and awas done separately 
			- awas version WITH <LOD correction 
			
	get_ratios_twp.ipynb
			- separate data into the UT and BL sections
			- get means for each flight and altitude grouping (e.g. UT for RF03 for each trace gas) 
			- save means 
			- use means to get ratios for all trace gases for each RF individually, as well as the campaign average 
			- add lifetimes to that data frame 
			- combine toga and awas into one “master list” pickle and save that 

	get_ratios_twp.ipynb
			- same as above but use awas version with <LOD correction 

	get_ratios_twp_varOH.ipynb
			- same as above but vary lifetimes according to bound of OH uncertainty 

##### get_tts
This folder is the bulk of the work for this project. Different iterations of ratios for which we determine a TTS. 
Python module in base_tts_code is used to calculate TTS and do plotting. 

	 figures 
		- repo to save all figures in 

	  tts_per_rf
		get_ratios_twp.ipynb
			- read in ratio data that saved mean per RF in the UT 
			- use campaign average BL to get ratios per RF 
		get_ratios_twp.ipynb 
			- read in outputs from get_ratios_twp 
			- get G(t) and and plot mu*-tau and G(t) for each RF 
		
	  tts_rf07 
		- close look at RF07, how does campaign average BL vs. RF07 BL affect ratios and results 

	  tts_vary_bl 
		fulldomain_bltau
			- vary bl height and see impact 
			- examine some individual flights closely (RF11, RF08, RF06)
			- look at shear line 
			- vary BL temporally and regionally 
		twp_bltau
			- same as above but only use data 0-25 N 
		twp_tropotau_varyregion
			get_ratios_varyregion.ipynb
				- see what happens when we compute ratios for BL = 0-10 N vs. BL = 0-25 N 
				- does changing BL from TWP focus vs. general tropics focus impact results?
			tts_vary_bl_varybl.ipynb
				- get G(t) and and plot mu*-tau and G(t) for each version 

	 tts_vary_tau
		tts_vary_tau.ipynb
			- get tts for campaign average UT and BL but with different lifetimes 
			- do not use <LOD correction for AWAS data
			- use all data north of equator 

		tts_vary_tau_twp.ipynb
			- get tts for campaign average UT and BL but with different lifetimes 
			- do not use <LOD correction for AWAS data
			- use only data 0-25 N 
			
		tts_vary_tau_twp_awas_replace.ipynb
			- get tts for campaign average UT and BL but with different lifetimes 
			- use <LOD correction for AWAS data
			- use only data 0-25 N 

		tts_vary_tau_twp_OHvar.ipynb
			- get tts for campaign average UT and BL but with different lifetimes 
			- do not use <LOD correction for AWAS data
			- use only data 0-25 N 
			- vary lifetime based on different OH values 

	 tts_vary_ut 
	My code gets confusing here, be warned. To do a fit for each segment for the whole campaign, the processing is a little hefty so I actually run this on modeling2 then transfer the results back to my local drive for plotting and playing with results. 

		get_tts_vary_ut_segments_total.ipynb
			- code that gets run on modeling2 because too hefty for me to run locally 
			- grab the files I made in /data_prep/ (below) and use them to get the tts for each segment 
			- each column in he data frame is one segment, with a ratio value for each trace gas 
			- get_tts for each column then save all outputs to access for plotting later 

		 data_prep 
			data_prep_ut_segments.ipynb
				- find all awas data in the UT, get the times of canister collection 
				- each awas can = 1 segment/sample 
				- co-locate toga data within +/- 3 minutes of awas canister 

			get_ratios_ut_segments.ipynb
				- use segment data to get ratios for each sample for toga and awas 
				- add lifetimes, combine to a master list to be used for input into “get_tts” 
				- save tracer name ordering for each segment, you’ll need it later
				- ordering will vary for each one because not all species are measured every segment. 

		 MD2_outputs
			Outputs from modeling2, used for plotting in directories below “plots_for_….” 

		 plots_for_campavgbl_bltau_fulldomain 
		 plots_for_campavgbl_bltau_twp 
		 plots_for_campavgbl_tropotau_twp 
		 plots_for_campavgbl_tropotau_twp_awas_replace
			plot_tts_vary_ut_segments.ipynb
				- read in output from modeling2
				- plot each segment mu*-tau and TTS in gray 
				- isolate extremes (min, max modes) 		
				- get average of all segments for segment average (black) 
				- plot box plot to show distribution of means and modes 
			plot_tts_vary_ut_segments.ipynb
				- read in output from modeling2
				- choose particular segments and plot them over all segments 
		 sameflightbl 
			Same as above but use same flight BL rather than campaign average BL 
			E.g. RF03 UT paired with RF03 BL to get ratio 
			Not recommended 

##### examine_ratios
	- statistics on ratios and distributions for some key species, ut and bl concentration comparison, etc 
	- nothing you really need unless youre interested in some of the chemical distributions 

##### regional_plots
	- various map plots, flight footprint, vertical sampling altitudes 

##### vertical_profiles 
	- various vertical profiles for a few select trace gases 

________________________________________________________________________________
## Sample order of operations 

Start to finish, basic outputs for one RF or for CAMPAIGN AVERAGE: 
1) contrast_readin - for both toga and awas, read in netcdfs 
2) get_ratios - to get “master list” data frames to be used, compute ratios per RF and for campaign average 
3) get_tts - for whatever combination of lifetime and ratio you want to use (pick appropriate columns from master list) 


________________________________________________________________________________
## Notes 

- You can avoid the steps 1 and 2 by just using file:
	/TTS_2020/get_ratios/contrast_ratios_two_awas_replace.pkl 

- For preliminary flight ranking results see: 
	/TTS_2020/get_tts/tts_per_rf/tts_vary_bl_per_rf.ipynb 

- THE LIFETIMES HERE ARE NOT THE FINAL VERSION, THERE ARE ERRORS IN THE INCLUDED LIFETIME VALUES. 
I will update this ASAP.  



