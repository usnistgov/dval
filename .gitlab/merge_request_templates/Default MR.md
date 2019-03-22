- [ ] Includes a summary of the purpose of the MR and commits
- [ ] Link to any issues that this MR addresses
- [ ] Includes tests
- [ ] (if needed) documentation was updated  
- [ ] Passes CI
- [ ] [When ready for code review] Added label `Review` (to both issue and MR)
- [ ] Code reviewer assigned to merge request
- [ ] Issue label changed from `Review` to `Ready` when MR is accepted by code reviewer.

# Instructions

### Developer

1. Open a MR at any time when working on an issue. The source branch should be your issue branch (naming irrelevant) and `develop`.
1. Make sure to include the label `Doing` on *both* the issue and MR.
2. Address the issue and make sure:
  * your code is readable and maintainable
  * your code includes tests
  * you updated any relevant documentation
  * your code passes the CI (automatic, look for :white_check_mark:)
  * you included a summary of your changes for the code Reviewer
  * you updated the progress  in the MR checklist
3. Change the `Doing` label in `Review` on the Issue and MR (Issue labels and MR labels are separate!!!)
3. Assign a code reviewer
3. (if the code reviewer asks) Start back at 2., make changes and send back to review


### Reviewer

Your role is to be a second set of eyes to check that everything as it should be.
This is also an opportunity to share insights on code readability, brevity, etc.

The code review is not an evaluation.

1. Check that :
  * you understand what this issue addresses
  * the CI pipeline passes
  * tests are present in the MR
  * the code is readable and you can follow the reasoning
  * any documentation was updated to reflect the changes
2. When appropriate, suggest actionable changes using the MR comments or the line-in-code comments
3. Asking for clarification is also O.K.
4. When you feel like the MR is ready, use the "Merge" button with the "delete issue branch" option (or delete the branch separately)
5. Change the Issue label from `Review` to `Ready`
