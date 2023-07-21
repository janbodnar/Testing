# Python-Tester
Python testing course


## Software characteristics 

- *Software reliability* describes the ability of a system to keep functioning under  
  specific use over a specific period.  
- *Software usability* is the degree of how the users find the software product easy to use.  
  It describes the overall user experience with the product.  
- *Fault tolerance* is the capability of the software product to maintain a  
  specified level of performance or to recover from faults such as software faults,  
  environment failures, wrong use of interface, or incorrect input.  
- *Software maintainability* is defined as the degree to which an application is understood,  
  repaired, or enhanced.  

## Processes 

 - *Linting*: the process of running a program that statically analyses code for potential errors.  
   The code in question is not run.  
 - *Debugging*: debugging is the process of identifying and removing errors from a computer program.  
   It localizes and corrects faults.  
 - *Software testing*:  process of checking the quality, functionality, and performance of the software  
   under test by validation and verification. The goal of testing is the systematic detection of failures.  

Linting and debugging is usually done by developers. Testing is done by testers. 


## Test types

- Unit test: checks a small bit of code, like a function or class. For instance, we check the validity
  of a price calculation.  
- Integration test: is a level of software testing where individual units/components  
  are combined and tested as a group. (We check if a function saves data into a database table.)  
- End-to-end test: a testing method that evaluates the entire application flow, from start to finish.
- Functional test: checks a single bit of software functionality, such as addition or deletion of a user.

## Test case 

A test case is a document which consists of a set of conditions or actions which are performed  
on the software application in order to verify the expected functionality of the feature.  

    Test Case ID 
    Test case Description/Summary
    Test steps 
    Pre-requisites 
    Test category
    Author
    Automation 
    Pass/fail
    Remarks


## Test coverage

Test coverage is a software testing metric that indicates the quantity of testing completed  
by a collection of tests. It helps identify areas that are missing or not validated.


## Functional vs nonfunctional testing  

Smoke Testing, Unit Testing, and Database Testing are all types of functional testing.  
Non-functional testing comprises the behaviour aspect of the system, i.e., performance, stress, etc.  
Performance testing, usability testing, and volume testing are all types of non-functional testing.  

## Smoke testing 

Smoke testing is a type of software testing that is typically performed at the beginning of the  
development process to ensure that the most critical functions of a software application are   
working correctly. It is used to quickly identify and fix any major issues with the software   
before more detailed testing is performed. The goal of smoke testing is to determine whether   
the build is stable enough to proceed with further testing. 

- Smoke testing is a type of software testing performed early in the development process
- The goal is to quickly identify and fix major issues with the software
- It tests the most critical functions of the application
- Helps to determine if the build is stable enough to proceed with further testing
- It is also known as Build Verification Testing or Build Acceptance Testing.


Smoke testing is also done by testers before accepting a build for further testing.

Smoke tests are a subset of test cases that cover the most important functionality of a component  
or system, used to aid assessment of whether main functions of the software appear to work correctly.  
Microsoft claims that after code reviews, smoke testing is the most cost-effective method for 
identifying and fixing defects in software.  

One can perform smoke tests either manually or using an automated tool.  

Smoke testing originated in the hardware testing practice of turning on a new piece of hardware  
for the first time and considering it a success if it does not catch fire and smoke. 




