# Created by nadavh at 15/01/2018
Feature: Connect to a cluster master and upload Amaterasu bundle
  # Enter feature description here

  Scenario: Connecting to a master with valid username and password

    Given A password enabled master node at localhost
    Given The SSH user-pass credentials: test:test
    When Trying to connect
    Then The connection should be successful

  Scenario: Connecting to a master with valid ssh key

    Given A private key enabled master node at localhost
    Given The SSH private key is 'amatest.pub'
    When Trying to connect
    Then The connection should be successful

  Scenario: Uploading Amaterasu bundle to master
    Given A password enabled master node at localhost
    Given The SSH user-pass credentials: test:test
    When Trying to upload Amaterasu bundle to /home
    Then A new directory named /home/amaterasu should exist on the master
    And /home/amaterasu/ama-local should be part of the user path

  Scenario: Uploading Amaterasu bundle to master without permissions
    Given A password enabled master node at localhost
    Given The SSH user-pass credentials: test:test
    Given /home folder has no permissions for the user
    When Trying to upload Amaterasu bundle to /home
    Then An exception should be thrown