# AppDownloads
Predict App downloads based on AppStore Rankings


[//]: # (Image References)
[image1]: ./output/SenseTower_1.png
[image2]: ./output/SenseTower_2.png
[image3]: ./output/SenseTower_3.png
[image4]: ./output/SenseTower_4.png
[image5]: ./output/SenseTower_5.png
[image6]: ./output/SenseTower_6.png
[image7]: ./output/SenseTower_7.png
[image8]: ./output/ActualVsPredicted.PNG

1) What are your initial observations about the ranking and download datasets?
	
	
	Ranking Dataset:
	
		○ Contains Top 400 ranked Apps list, sampled every hour, over two week(13/5/14 - 30/5/14) period.
		○ Sampling performed across the regions -- USA, Great Britain and South Africa. 
		○ Data collected from IOS App store for both iPhone and iPad.
		○ Data quality issues like non-uniform sampling resulted in some missing data points.
		○ Dataset has ranking information for over 2200 apps across 3 regions and 2 devices
	
	
	Download Dataset :
	
		○ Dataset has total daily downloads information for 140 Apps.
		○ # downloads captured at granular level of 3 regions and 2 devices for two weeks period.




2) What patterns do you see in the download dataset?

	Ranking Dataset:

		○ Quantity of data collected for first couple of days is significantly less compared to the rest.
		○ Interestingly, for most of days, ranking data at 16th and 20th hour was missing for GB region. 
		○ Daily, equal number of data points were gathered for iPad and iPhone.

	![alt_text][image1]
		
		○ Observing a sample of 100 Apps, only a fraction of Apps appear in Top-400 list on both devices.
			§ An inference would be, either some Apps were built for both iPad and iPhone, (or)
			§ Some Apps were popular on iPhone or vice-versa.
		○ More or less, Apps has proportional presence across 3 regions.
	
	![alt_text][image2]
		
	Downloads Dataset:
		
		○ 70% of downloads happening on iPhone -- trend is consistent on daily basis.
		○ People from USA does ~78% of overall downloads.
		○ 56% of total downloads happen on iPhone from USA region.
		○ Upward download trend is observed over two week monitoring period.
		
	![alt_text][image3]

	![alt_text][image4]



3) Which segments should you divide the data into before analyzing the relationship between ranks and downloads?

	• I would divide data by Country, by Device for further analyze relationship between ranks and downloads


For the following questions, answer them for a segment of data on a date. (Pick whichever segment or date you want)


4) What is the relationship between ranks and downloads?

	• To start with, I see downloads are inversely related to rank. Lower the rank higher the downloads.
	• I would further investigate whether this relationship is kind of Linear/Log.

![alt_text][image5]



5) What is the best measure to use to calculate an average daily rank for an app from its hourly ranks? (Mean, Median, Harmonic Mean, etc.)

	• Mean, Media correlation plot shows larger daily rank spread for Apps ranked 150 or higher.
	• From Mean, Hmean correlation chat, Amean forms the upper bound -- so, it's realistic to consider Hmean.
	• Also, the sampled rank is hourly standings, Hmean is the appropriate central tendency we should be considering.  


![alt_text][image6]
	
![alt_text][image7]



6) Create a model to predict downloads from average daily rank.

		○ From previous observations, it's evident, we see positive linear relationship between Date(time) and downloads.
		○ Downloads are related to Rank as -log(a0*Rank).
		○ As of now I'm seeing a model like,   Downloads = f(Days, Rank, Country) -- Unique model per device.
		○ Train/Test split : As downloads show time(day) dependancy, will trip last 3days data for testing
	

7) Evaluate the model.
	•      Model has R2 of 0.76 on test data.

![alt_text][image8]


## Observations:
	1. Linear model can explain downloads to an accuracy of 76% -- Model restricted to 'DaysLapsed' and 'Ranking'.
	2. Predictions error-variance is high for top-50 ranked App downloads -- Downloads for top-50 apps are exponential.
	3. Ln(lambda*HmeanRank) would be interesting proposition to try for Accuracy improvement.
