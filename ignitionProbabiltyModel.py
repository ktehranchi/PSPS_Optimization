from operator import index
import pandas as pd
import numpy as np
import os
from os import path
from elapid import geo, models, utils
from matplotlib import pyplot as plot
import seaborn as sns
import rasterio


windData_path = os.path.join(os.getcwd(),'Data/PGE_VegFire_windData.csv')
windData= pd.read_csv(windData_path)
windData = windData[ ~ windData.wind_speed.isna()]
windData = windData[ ~ windData.wind_speed_max.isna()]
windData = windData[~ windData.wind_speed.str.contains("no data")]
windData.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'date', 'year', 'month', 'day', 'time','hour', 'minute','suppressed_by', 'suppressing_agency','facility_identification', 'other_companies', 'was_there_an_outage','date_1', 'time_1',  'contact_from_object','facility_contacted', 'unnamed_23','material_at_origin_comments'],inplace=True)
windData.wind_speed = windData.wind_speed.astype(float)

abs_windData_path = os.path.join(os.getcwd(),'Data/abs_windData.csv')
abs_windData= pd.read_csv(abs_windData_path).drop(columns='Unnamed: 0')
abs_windData.dropna(inplace=True)

y_true= np.ones(shape=windData.shape[0])
y_false= np.zeros(shape=abs_windData.shape[0])
y=pd.DataFrame(np.append(y_true,y_false),columns=['label'])

x_true= windData.wind_speed.values
x_false= abs_windData['0'].values
X=pd.DataFrame(np.append(x_true,x_false),columns=['wind_speed'])

# sns.histplot(windData.wind_speed)
# sns.histplot(y)

#Fit Model
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomTreesEmbedding
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay

X_full_train, X_test, y_full_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=10
)
X_train_ensemble, X_train_linear, y_train_ensemble, y_train_linear = train_test_split(
    X_full_train, y_full_train, test_size=0.5, random_state=10
)

n_estimators = 10
max_depth = 2

random_tree_embedding = RandomTreesEmbedding(
    n_estimators=n_estimators, max_depth=max_depth, random_state=0
)

rt_model = make_pipeline(random_tree_embedding, LogisticRegression(max_iter=1000))
rt_model.fit(X_full_train, y_full_train)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_full_train, y_full_train)

fig, ax = plt.subplots()
models = [
    ("RT embedding -> LogReg", rt_model),
    ("LogReg Only", lr_model),
]

model_displays = {}
for name, pipeline in models:
    model_displays[name] = RocCurveDisplay.from_estimator(
        pipeline, X_test, y_test, ax=ax, name=name
    )
_ = ax.set_title("ROC curve")
plt.show()

#plot logistic fit curve
from scipy.special import expit
plt.figure()
plt.scatter(X.values.ravel(), y, color="black", zorder=20)
X_test = np.linspace(-5, 80, 300)
loss = expit(X_test * lr_model.coef_ + lr_model.intercept_).ravel()
plt.plot(X_test, loss, color="red", linewidth=2)
plt.ylabel("Probability of Ignition")
plt.xlabel("WindSpeed")
plt.show()




########### ELAPID ######################
import geopandas

vector_path = "GIS/PGE_veg_ignitionpoints.shp"
vegCover_path = os.path.join(os.getcwd(),'GIS/treeheight_20m_mask.tif')

output_raster_path = "/home/slug/ariolimax-californicus-habitat.tif"
output_model_path = "/home/slug/ariolimax-claifornicus-model.ela"

src= rasterio.open(vegCover_path)
plot.imshow(src.read(1),cmap='pink')


# x_sample, y_sample = utils.load_sample_data()
# model = models.MaxentModel()
# results = model.fit(x_sample, y_sample)

# sample the raster values for background point locations
pseudoabsence_points = geo.sample_raster(vegCover_path, count=26421)

# read the raster covariates at each point location
presence = geo.annotate(vector_path, vegCover_path)

pseudoabsence = geo.annotate(pseudoabsence_points, vegCover_path)

# # merge the datasets into one dataframe
# pseudoabsence['presence'] = 0
# presence['presence'] = 1
# merged = presence.append(pseudoabsence).reset_index(drop=True)
# x = merged.drop(columns=['presence'])
# y = merged['presence']

# # train the model
# model = elapid.MaxentModel()
# model.fit(x, y)

# # apply it to the full extent and save the model for later
# elapid.apply_model_to_rasters(model, vegCover_path, output_raster_path, transform="cloglog")
# elapid.save_object(model, output_model_path)