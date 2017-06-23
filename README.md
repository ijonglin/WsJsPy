# WsJsPy
Copyright I-Jong Lin 2017
## Websockets/Javascript/Python Framework For Full Stack Development
### Statement of Purpose
A minimal short stack of components for full application development that can be prototyped by one person and then farmed out to domain experts as time goes on.   The key qualities of this particular framework is as follows:
* End-to-end prototype functionality and system testing can be achieved by one or two developers who have knowledge of only two languages (Javascript and Python)
* System componentization of the framework allows for addition of other developers to substitute their own components and add their own domain specific infrastructure and languages into the system
* Primary of separate concerns: UI and hardware abstraction of back-end services to enforce overall MVC pattern  
* Explicit communication layer between these two concerns is Websockets and Json; the system transport layer may then be replaced with an optimized communication framework.  The key aspect is that communication between concerns be explicit and defined in a schema between the two dynamically typed languages, bootstrapping with JSONSchema

## Philosophy
With the Internet and Software technologies embedded into the daily infrastructure of our lives, I believe the challenge of system design has moved from an 
technological problem to an organization problem.  For better or for worse, the technologies that are being rendered into the Software are no longer software technologies.
Software development is powerful enabling technology and enables an individual or a small team of individuals to attain incredible prototype functionality with little or no 
capital investment (or even the purchase of any software licenses, thank god!), by easily shifting and connecting information from processes and hardware in ways that were not
conceivable a few years ago.   These technologies (for instance, in the biotech field) are actually more complex than software technologies themselves, but software development
provides the key tool to manage this complexity.

The prototype (or Proof of Concept, in Adobe Terminology) contains the definition of the end-to-end system functionality in its purest form.   However, 
when the prototype needs to be scaled out to millions of users, deployment of this technology also becomes complex in and of itself and once again.  Once again,
software development provides the means to manage this complexity.

> _The trap is when software development for deployment and scalability becomes beholden to deployment and scalability complexity._ 

The equivocation of domain expertise and software expertise becomes downfall of the system; both are required for successful product development, but product definition
needs to remain separate and distinct from its deployment infrastructure.  When the product __IS__ software, this separation can often be blurred as the domain expertise 
can be organically shared between personnel and the separation can be understood implicitly between all software professionals.  However, when the product is different
than software and often requires a domain expertise that is foreign to a software developer, the functionality of the system needs to be maintained and expressed in 
a software-testable manner in order to maintain its integrity of end-to-end system function.

Philosophically, WsJsPy is _a_ solution to this separate the concerns of deployment and functionality.   The architecture of WsJsPy expresses the system-functionality 
through system component testing, and can maintain the integrity of system functionality by serving as the functional prototype __and__ the bootstrapping layer for 
system component testing.   It is hoped that many future upgrade paths for different system aspects (security, scalability, fault tolerance, etc.) will be developed 
for this project, but at its core, this solution (or a solution like WsJsPy) will exist at the kernel of a well-designed system. 

# Setting Up WsJsPy

# Development in WsJsPy

# Upgrade Paths in WsJsPy

## Security
## Scalability
## Persistence
## Hardware Integration
## UI Componentization

# Colophon

## Pronounciation
Pronounced _Wuz-Just-Pie_; it can optionally be accompanied by a sheepish grin of someone who just ate a whole pie.  Also a good mnemonic for whether its prefix
ordering of components: Ws (Websockets), comes before Js (Javascript) comes before Py (Python).

Copyright I-Jong Lin 2017
