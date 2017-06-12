var skills = [
    { "name": "Java", years: 11, "relevancy": 1.3 },
    { "name": "JavaScript", years: 14, "relevancy": 1 },
    { "name": "Nightwatch", years: 3, "relevancy": 1 },
    { "name": "PhantomJs", years: 3, "relevancy": .7 },
    { "name": "jasmine", years: 2, "relevancy": 1.1 },
    { "name": "qunit", years: 1, "relevancy": .8 },
    { "name": "HTML", years: 15, "relevancy": .7 },
    { "name": "PHP", years: 2, "relevancy": .5 },
    { "name": "CSS", years: 14, "relevancy": .7 },
    { "name": "Flash", years: 9, "relevancy": .2 },
    { "name": "Actionscript", years: 9, "relevancy": .3 },
    { "name": "Flex", years: 1, "relevancy": .2 },
    { "name": "Delphi", years: 3, "relevancy": .3 },
    { "name": "Apache", years: 3, "relevancy": .75 },
    { "name": "IBM WebSphere", years: 3, "relevancy": .75 },
    { "name": "Tomcat", years: 2, "relevancy": .75 },
    { "name": "Oracle OC4J", years: 1, "relevancy": .5 },
    { "name": "Jetty", years: 2, "relevancy": .75 },
    { "name": "JUnit", years: 8, "relevancy": .8 },
    { "name": "Struts", years: 2, "relevancy": .3 },
    { "name": "Spring", years: 7, "relevancy": 1.3 },
    { "name": "J2EE", years: 7, "relevancy": 1 },
    { "name": "JPA", years: 4, "relevancy": .8 },
    { "name": "Hibernate", years: 4, "relevancy": 1 },
    { "name": "EclipseLink", years: 2, "relevancy": 1 },
    { "name": "JMock/EasyMock", years: 5, "relevancy": .8},
    { "name": "JSF", years: 6, "relevancy": .9 },
    { "name": "Facelets", years: 6, "relevancy": .5 },
    { "name": "Richfaces", years: 6, "relevancy": .5 },
    { "name": "Flying Saucer", years: 1, "relevancy": .5 },
    { "name": "JAXB", years: 5, "relevancy": .8 },
    { "name": "JAXWS", years: 2, "relevancy": 5 },
    { "name": "SOAP", years: 2, "relevancy": 5 },
    { "name": "Apache commons", years: 6, "relevancy": .75 },
    { "name": "Google Guava", years: 4, "relevancy": .75 },
    { "name": "Jackson", years: 1, "relevancy": .6 },
    { "name": "Jersey", years: 1, "relevancy": .6 },
    { "name": "KnockoutJs", years: 3, "relevancy": .8 },
    { "name": "Mustache", years: 1, "relevancy": .6 },
    { "name": "HandlebarsJs", years: 2, "relevancy": .6 },
    { "name": "Sammy", years: 3, "relevancy": .7 },
    { "name": "RequireJs", years: 3, "relevancy": 1 },
    { "name": "ANT", years: 9, "relevancy": .8 },
    { "name": "CVS", years: 2, "relevancy": .3 },
    { "name": "Subversion", years: 8, "relevancy": .5 },
    { "name": "SVN", years: 8, "relevancy": .5 },
    { "name": "GIT", years: 4, "relevancy": .8 },
    { "name": "Maven", years: 5, "relevancy": .5 },
    { "name": "IBM ClearCase", years: 2, "relevancy": .3 },
    { "name": "JSP", years: 4, "relevancy": .3 },
    { "name": "Servlets", years: 5, "relevancy": .5 },
    { "name": "XML", years: 13, "relevancy": .5 },
    { "name": "DTD", years: 3, "relevancy": .5 },
    { "name": "XML SAX", years: 3, "relevancy": .4 },
    { "name": "XML DOM", years: 11, "relevancy": .4 },
    { "name": "xpath", years: 4, "relevancy": .7 },
    { "name": "Cruisecontrol", years: 3, "relevancy": .3 },
    { "name": "RegEx", years: 6, "relevancy": .5 },
    { "name": "UML", years: 5, "relevancy": .7 },
    { "name": "Agile", years: 7, "relevancy": .8 },
    { "name": "Scrum", years: 6, "relevancy": 1 },
    { "name": "Kanban", years: 1, "relevancy": .8 },
    { "name": "MySQL", years: 8, "relevancy": .8 },
    { "name": "Oracle", years: 2, "relevancy": .7 },
    { "name": "DB2/AS400", years: 2, "relevancy": .7 },
    { "name": "Linux", years: 3, "relevancy": .2 },
    { "name": "Windows", years: 21, "relevancy": .2 },
    { "name": "Android", years: 2, "relevancy": .5 },
    { "name": "WSAD5", years: 2, "relevancy": .3 },
    { "name": "RAD6", years: 2, "relevancy": .3 },
    { "name": "Eclipse IDE", years: 8, "relevancy": .5 },
    { "name": "Docker", years: 1, "relevancy": 1 },
    { "name": "ActiveMq", years: 3, "relevancy": .8 },
    { "name": "RabbitMq", years: 1, "relevancy": .8 },
    { "name": "IntelliJ", years: 2, "relevancy": .5 },
    { "name": "WebStorm", years: 2, "relevancy": .5 },
    { "name": "Grunt", years: 3, "relevancy": 2 },
    { "name": "gulp", years: 2, "relevancy": 2 },
    { "name": "WebPack", years: 1, "relevancy": 3 },
    { "name": "bootstrap", years: 1, "relevancy": 1.5 },
    { "name": "angularjs", years: 4, "relevancy": 2 },
    { "name": "jquery", years: 10, "relevancy": 1 },
    { "name": "lodash", years: 3, "relevancy": .9 },
    { "name": "underscore", years: 3, "relevancy": .8 },
    { "name": "sammy", years: 4, "relevancy": 1 },
    { "name": "knockoutjs", years: 4, "relevancy": .8 },
    { "name": "requirejs", years: 4, "relevancy": 1.2 },
    { "name": "commonjs", years: 1, "relevancy": 1.2 },
    { "name": "jms", years: 8, "relevancy": .7 },
    { "name": "rest", years: 6, "relevancy": .6 },
    { "name": "nodejs", years: 2, "relevancy": 1 },
    { "name": "npm", years: 3, "relevancy": .8 },
    { "name": "bower", years: 3, "relevancy": .5 },
    { "name": "cloud9", years: 4, "relevancy": .5 },
    { "name": "Amazon AWS", years: 2, "relevancy": .7 },
    { "name": "AWS Route53", years: 1, "relevancy": .75 },
    { "name": "AWS CloudFront", years: 1, "relevancy": .75 },
    { "name": "Fitnesse", years: 1, "relevancy": .75 },
    { "name": "AWS EC2", years: 2, "relevancy": .75 },
    { "name": "AWS Lambda", years: 1, "relevancy": .75 },
    { "name": "AWS S3", years: 2, "relevancy": .75 },
    { "name": "C#", years: 1, "relevancy": .3 },
    { "name": "Alfresco", years: 1, "relevancy": .3 }
]