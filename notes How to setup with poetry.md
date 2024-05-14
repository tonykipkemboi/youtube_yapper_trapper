#### CrewAi with poetry

[Create a Custom Tool to connect crewAI to Binance Crypto Market](https://youtu.be/tqcm8qByMp8?si=71vmdqCj57a2zkSW&t=101)

myCrewAiProjects> git clone https://github.com/tsktech/youtube_yapper_trapper.git
myCrewAiProjects> cd youtube_yapper_trapper
myCrewAiProjects\youtube_yapper_trapper> code .
if the conda env is not set then (btw i use this env .crewai for all my crew proj)
myCrewAiProjects\youtube_yapper_trapper> conda create -n .crewai
(.crewai) myCrewAiProjects\youtube_yapper_trapper> conda activate .crewai 
(.crewai) myCrewAiProjects\youtube_yapper_trapper> pip install crewai[tools]

#### we dont have to create the project but just for learning (**we have cloned the repo**)
(.crewai) myCrewAiProjects\youtube_yapper_trapper> crewai create youtube_yapper_trapper
(.crewai) myCrewAiProjects\youtube_yapper_trapper> conda deactivate
(base) myCrewAiProjects\youtube_yapper_trapper> code .

#### right click on youtube_yapper_trapper folder open in code new window
#### cause poetry creates the env for the project we dont require the conda env
***note we are not in the conda env .crewai***

myCrewAiProjects\youtube_yapper_trapper> poetry shell
*** Spawning shell***
*** within C:\Users\sos\AppData\Loca1\pypoetry\Cache\virtua1envs\youtube_yapper_trapper-XXXX-py3.10 ***
if needed add dependency
(youtube_yapper_trapper-py) myCrewAiProjects\youtube_yapper_trapper> poetry add load-dotenv pandas 
this will install the dependency and create the lock file.
#### however cause we have cloned the repo
follow [same video diff time](https://youtu.be/tqcm8qByMp8?si=nQj2ToryCqPVZInh&t=742)
(youtube_yapper_trapper-py) myCrewAiProjects\youtube_yapper_trapper> poetry lock
(youtube_yapper_trapper-py) myCrewAiProjects\youtube_yapper_trapper> poetry install
(youtube_yapper_trapper-py) myCrewAiProjects\youtube_yapper_trapper> **poetry run youtube_yapper_trapper**



