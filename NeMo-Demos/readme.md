## Steps to run for the first time, to create the project, model and service
* First, in your 'projects' tab, you will need to create a new project
* Type the name and the description of the project. Optionally, you can add some tags
* In the second step of the project creation, you will be able to add the NGC models that will be used: 
  * Click in create a new asset, type the for the asset, select NGC MODEL and asset type, and add the catalog name of the models in the ‘available models’ box
  * The models that will be used in this demo are
    * **Asset Name**: STT-Citrinet - **Model**: STT En Citrinet 1024 Gamma 0.25
    * **Asset Name**: en-es-transformer – **Model**: NMT En Es Transformer12x2
    * **Asset Name**: FastPitch-HiFiGAN – **Model**: TTS Es Multispeaker Fastpitch HiFiGAN
  * Using the asset name given here will make sure that the correct folder is referenced on the experiment code. Using different asset names may require adapt the code
  * **Warning**: Avoid adding the same NGC asset twice, with different asset names. This will cause the actual files to be corrupted.
* Finish creating the project
* Inside the project, in the tab setup and documentation, add the Github Repo https://github.azc.ext.hp.com/phoenix/ds-experiments
  * Click in clone
  * Fill the Git repo URL with the URL above
  * Add a local folder where the repo will actually be downloaded
  * Click in Clone Github Repo
* In the overview tab of the project create a new NGC workspace: 
  * Click in New Workspace
  * Select the first card Nvidia NGC
  * Type a name for the workspace and click in Create Workspace
* Start your new workspace by clicking on the "play" button on the card
* After started open the workspace by clicking on the "terminal" button on the car
* Inside Jupyter lab, find the nemo-demos folder on your file system (you might need to manually switch to the proper branch)
* Open the AudioTranslationSample.ipynb notebook
* Run all the cells on the notebook. This should, among other things, log and register the model in MLFlow
* Go to the Published Services tab and create a new service 
  * Select nemo_en_es as the model
  * Choose the latest version
  * Choose a name to the service and click on Deploy

## Steps to run after the service is created for the first time 
* To start the service, click on the "play" button in the row of the service you created
* After it finishes loading (might take some minutes), a URL link will be shown on the same row. Clicking on that URL will open Swagger on your browser 
  * In the top part of swagger screen, there should be a link to open the demo - it will load the web client

