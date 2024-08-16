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
  2.1.1. Create a new issue
     * On the top-right of the issue page, there is a "new issue" button. Clicking this will redirect you to the issue creation page. Here you can enter a title and short description of the  issue. Name the issue in the title slot and add a description. *E.g. Title: Printing bug Des: error raised when printing stats*
     * After this, you can add labels also before creating. (See 4)
     * When you are finished, click on the green "submit new issue" button.
  2.1.2. Assign yourself to an existing issue
     * To assign yourself to an issue, *(which means that you are going to fix it)* click on the issue name on the issues page. This should open the issue's details. At the top of the list on the right of the page there should be a Assignees section. Click the gear icon next to it to open a dropdown menu, where you can assign the issue to yourself.
  2.1.3. Add labels to an issue
     * Click on the issue name on the issues page. This should redirect you to the issue's details. On the right side of the page, there is a label section. Click on the gear icon next to it and it should pop up with a dropdown menu. Here you can add or remove issues. Refer to the issue description when deciding which labels to add to the issue.
### 2.2 Branches
When you have assigned yourself to an issue (see 2.1.2), its time to start coding! <br>
Go to VS code and open the folder with the repository. (see 1.1) In the terminal write `git checkout -b "[Your branch name (see next for formatting)]"` You should name your branch as `[Your Name]-[Shortened version of issue]` This should make a new branch, which is where you will edit the code so that you don't edit the main branch. Now you can edit code and fix the issue! <br>
These are some other commands that are useful:
  * `git checkout -b [branch name]` This is to make a new branch and switch to it. (see above)
  * `git checkout [branch name]` This is to switch branches. You must commit before you do this. (see 2.3)
  * `git branch` This gives you a list of all your branches, and highlights the one you are on.
### 2.3 Commiting and Pushing
### 2.4 Pull Requests
