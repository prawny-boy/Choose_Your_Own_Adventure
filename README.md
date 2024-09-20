*This is a Choose Your Own Adventure game made by Sean, Oliver and Levi.*
*This is a documentation on how to use it. (Version 1.0)*
## 1. Getting Started
### 1.1 Cloning
To get started with this repository, make a new empty folder and open it in VS code.
Go to this repository and click on the "code" tab. On the top right there should be a green "code" button. Clicking that should open a dropdown menu where you need to copy the link it displays. After this, return to VS code and enter `git clone [link you copied]` into the terminal. You have now opened all the code in the "main" branch of the repository.
*If you are having issues finding the terminal, click the view button on the top left and then click terminal.*

![image](https://github.com/user-attachments/assets/e951ae34-c6e6-4cdf-bc7f-63845c27bd28)
### 1.2 Understanding
Read through all the code and understand it before moving on.

## 2. Editing
So you want to contribute to the code? This is how you can go about it properly.

### 2.1 Issues
Usually, the first thing you do is look at issues, so that you can fix the code. On the repository page, click the "issues" tab. Here are the issues that other people working on the code (contributers) can work on. You will soon become one of them! You can do a few things with issues:
#### 2.1.1 Creating a new issue
On the top-right of the issue page, there is a "new issue" button. Clicking this will redirect you to the issue creation page. Here you can enter a title and short description of the  issue. Name the issue in the title slot and add a description. *E.g. Title: Printing bug Des: error raised when printing stats*
After this, you can add labels also before creating. (See 4)
When you are finished, click on the green "submit new issue" button.
#### 2.1.2 Assigning yourself to an existing issue
To assign yourself to an issue, *(which means that you are going to fix it)* click on the issue name on the issues page. This should open the issue's details. At the top of the list on the right of the page there should be a Assignees section. Click the gear icon next to it to open a dropdown menu, where you can assign the issue to yourself.
#### 2.1.3 Add labels to an issue
Click on the issue name on the issues page. This should redirect you to the issue's details. On the right side of the page, there is a label section. Click on the gear icon next to it and it should pop up with a dropdown menu. Here you can add or remove issues. Refer to the issue description when deciding which labels to add to the issue.

### 2.2 Branches
When you have assigned yourself to an issue (see 2.1), its time to start coding! <br>
Go to VS code and open the folder with the repository. (see 1.1) In the terminal write `git checkout -b "[Your branch name (see next for formatting)]"` You should name your branch as `[Your Name]-[Shortened version of issue]` This should make a new branch, which is where you will edit the code so that you don't edit the main branch. Now you can edit code and fix the issue! <br>
These are some other commands that are useful:
  * `git checkout -b [branch name]`: This is to make a new branch and switch to it. (see above)
  * `git checkout [branch name]`: This is to switch branches. You must commit before you do this. (see 2.3)
  * `git branch`: This gives you a list of all your branches, and highlights the one you are on.

### 2.3 Commiting and Pushing
#### 2.3.1 Commiting
After you edit the code, and finish one thing (this doesn't neccessarily have to finish the whole issue), you can commit to save your work so that you can get it back later. <br>
To commit, run these commands in terminal:
  1. `git add .`: This prepares the changes to be commited
  2. `git commit -m "[Summary of your changes/commit message]"`: This commits all the readied code. Enter a commit message so that other people know what you changed. Please don't use "more code" as a commit. Be sensible about what you put in the message.
#### 2.3.2 Pushing
*Before doing this step, make sure to commit! (see 2.3.1)* <br>
To save code onto github, you have to push. <br>
You can do this by running this command in terminal: `git push origin [branch name you are on]` *(If you don't know what branch you are on use `git branch` or see 2.2)*

### 2.4 Pull Requests
*Only do this after Commiting & Pushing (see 2.3)*
#### 2.4.1 Making Pull Requests
Once you have pushed to github, you can go to the repository page and into the code tab. There you should see a orange-ish bar saying "[branch name] had some recent pushes x minutes ago". *(If this doesn't show up try reloading the page)* Click on the "compare & pull request" button and it should open a page to create a pull request. Name it as "[Your name] - ["Issue/Topic"]". You can also add details but it is not neccessary. Click the green button at the bottom-right "create pull request".
#### 2.4.2 Adding Issues to Pull requests
Because Pull Requests are used to solve issues, you need to assign an issue to each Pull Request. To do this, go to the repository page, then click the pull request tab/page, and click the Pull Request that you want to add an issue to. This should redict you to its details. On the right side is a list, and in that list find the Development section. Click the gear icon next the the section and a dropdown menu should appear, so that you can select or deselect the issues that the pull request is fixing. <br>
**Note: If you see a merge button, please do not click it without Sean's permission.**

### 2.5 Pulling
It is a good practice, to once in awhile, pull from github. Pulling is when you pull from the main branch to update your branch to the newest version of the game. <br>
You can do this by running `git pull origin main` <br>
After doing this there may be merge confilcts, so go through the files and accept which one is best.

## 3. Others
### 3.1 Testers
Get testers for the game so that any bugs can be fixed!
