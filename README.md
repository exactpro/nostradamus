<img src="https://github.com/exactpro/nostradamus/blob/media/logo/main_logo_blue.png?raw=true" width="450" height="150">

---

🧠 An open source machine learning application for analyzing software defect reports extracted from bug tracking systems.

Nostradamus is an open source application for analyzing software defect reports extracted from bug tracking systems.
The application uses Machine Learning techniques to determine important links between various defect attributes and generate certain bug metrics, such as the probability of:
* ❌ a bug being rejected;
* ✅ a bug being fixed, including time to resolve;
* 📝 a bug belonging to a specific area of testing.

Nostradamus also calculates various statistical data including distributions and values of aggregate functions and performs analysis of bug descriptions and, as a result, produces the following metrics:
* a list of the most frequently used terms;
* a list of the most significant words, etc.

This knowledge further allows to achieve various IT-related goals, e.g.:
* 📝 More accurate planning and goal setting for Project Managers;
* 📈 Improving the defect report quality for QA Engineers and Junior Analysts;
* 🔎 Discovering the dependencies hidden in development, for system architects and developers.

***

## Getting started

### System requirements

For best performance, please make sure that your machine satisfies all the recommended requirements:
* 2+ CPU
* 4Gb+ RAM 
* 10Gb+ HDD

### Installation

We use Docker to simplify the application infrastructure maintenance, so make sure that you have Docker installed on your machine.

**Prerequisites**

Specify your Jira-user credentials in the `.env` file to make Nostradamus able to interact with your data, e.g.:
* `JIRA_URL=https://jira.atlassian.com` _(no slash at the end)_
* `JIRA_USERNAME=username`
* `JIRA_PASSWORD=password`

**Build the images**
```shell script
docker-compose build
```

**Fire up the containers**
```shell script
docker-compose up -d --scale worker=3
```

You are all set! 🚀

The application is up and running on localhost.
Please navigate to `127.0.0.1` to start analysing your data.

***

## Where to get help

Please read our [Wiki page](https://github.com/exactpro/nostradamus/wiki) that covers most of the popular questions regarding the application's behavior.

You are always welcome to reach us via:
* 📮 our email-address: `nostradamus@exactprosystems.com`
* ⌨️ direct message to [@il1tvinov](https://github.com/il1tvinov) 