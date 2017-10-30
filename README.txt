Motong Chen
BotForSecurity

I develop this Bot based on Slack. This Bot can execute 5 different commands and there is hierarchy among these commands. The user can only excute some command after excecuting another one so that we make sure there would be less input error (i.e. random wrong ID user makes up). Here are the commands:

1. Counts: return how many data entries do we have
         subcommand: Sample <NUM>
2. Severity: Get events with specified severity (low, medium, high)
         subcommand: Specific <ID>
3. Search: Search for a specific keyword and get info
         subcommand: Specific <ID>

The subcommand could only be executed right after the master command be executed. However, if a user wrongly give parameter to a subcommand, he could still try this subcommand although it is not right after the master command.

If the user enter an invalid command that is undefined, the Bot would output all the commands again to remind the user about the correct command.

The behaviors of different command:
1. Counts:
This command simply asks the Bot to output how many CVE entries 
1.1 Sample
This command sample some random CVE descriptions to let the user get some idea what kind of data we have in our database

2. Severity
This command gives the user the information of all the CVE entries that has the severities the user specified. The user may be interested in events that have a certain severity. There are three levels: (low, medium, high). Note that not all CVE entries contain severity info so we have to do exception check to prevent the program from crashing.
2.1 Specific
After seeing a list of events, the user can spefify to see one specific one by it's ID. We will give more detailed info about that event, including the reference links so that user could get some outside source.

3. Search
The user could search for a specific keyword in the description of events because they might be interested in a specific company or website or product.
3.1 Specific
Same with the Specific in Severity.

Testing:
Update: I will be implementing the unit testing and integrated testing very soon. I have set up travis and read into how to do unit testing. (I hope it is okay to keep improving my project even after deadline)

I don't really know how to do unit testing with Slack in code actually but I did test my functionalities one by one. I implemented them by first created the skeleton that specify all the command I want to implement and then implement them one by one. For each functionality, I refract out the kernal code for it into a new helper method so that I could later maintain it and modify it more easily without creating destruction to other part. I tested each one of them after finishing its implementation. After finishing all the functionalities of it, I tested it integratively on Slack also. 

Because I separate out all the functionalitied, I think I could probably do unit test in code by not sending response to Slack but just do some local testing of my result. I do not have enough time for this now but it could be easily done later and I will keep improving my program further. 
