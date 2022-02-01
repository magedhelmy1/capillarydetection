# Contributing to HDMIA:

We love your input! You can contribute to the project the following way:

- Bug Reporting
- Submitting a fix
- Propose new feature(s)
- Becoming a maintainer

We use Github to track all of the above under the [issues tab](https://github.com/magedhelmy1/capillarydetection/issues).
We have templates to standardize the pull requests.

### Bug Reporting, Propose Feature(s) and Submitting a fix

There are templates available in the [issues tab](https://github.com/magedhelmy1/capillarydetection/issues).
Click "New Issue" and Select either a "Bug Report" or "Feature Request".

In addition, please use the following labels in the pull request so it is easy to filter it amongst other issues.

* Bug: Something is not working
* Enhancement: New feature or request
* Dependencies: Pull requests that update a dependency file
* Documentation: Improvements or additions to the documentation
* Help wanted: Need help understanding a part of the code of the GUI
* Question: Further information is requested

### Files that can be changed by contributors vs. files that are auto-generated

All the contents of the files in the project can be changed.
The docker build command will then auto-generate the server, API, database and frontend based on the code change.
Changing the structure of folders is possible but might raise warnings and errors.
The project structure is highlighted [here](https://github.com/magedhelmy1/capillarydetection#project-structure)

### How to test changes with an example file.

When changes are made to the code, there are two consoles the user can inspect to ensure it works correctly.

The following command builds the whole project, so they will show up here if there are errors.
This command also creates the sample files for the GUI, so the developer can check if the system can process the image successfully.

` docker-compose up -d –-build
`
When a code change is pushed to the repo, the following is triggered automatically, and the console output can be monitored from the Github action.
This is the pre-build stage before deploying to production and emulates an environment similar to production.


` docker-compose -f docker-compose.ci.yml build web react nginx tfserving_classifier_hsv tfserving_classifier_ssim
`

If the above is successful, a repo maintainer is notified to make the final pull request into main after checking the code.

To test with a sample file, navigate to the GUI, select any samples, and click "Analyze Sample Image". The GUI, after some seconds, should display three images. The original image, the analyzed image, and the segmented image with the number of capillaries and
capillary density under the image.

### Discussions

If you would like to discuss a feature or other related topics not covered above, please feel free to post it in
the [discussion area of the repo found here](https://github.com/magedhelmy1/capillarydetection/discussions/41).

## Becoming a maintainer

You want to maintain the code; this is fantastic!
Please send an email to magedaa@uio.no to discuss your availability and support you in any way to help maintain the repo.

## License
By contributing, you agree that your contributions will be licensed under its Attribution-NonCommercial 4.0 International.
More information can be found under the [license file of this project](https://github.com/magedhelmy1/capillarydetection/blob/master/LICENSE.md).
