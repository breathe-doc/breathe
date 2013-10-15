/**
* An Objective-C category
*
* Can be handled by breathe like a class, but is a rather unique extension method for adding methods to other classes.
*/
@interface NSObject (TestCategory)
/**
* An instance method.
*
* Adds a message that can be sent to instances of the category target.
* @param testArgument An object argument.
* @returns An object.
*/
- (NSObject *) testMethod:(NSString *)testArgument;
/**
* A class method.
*
* Adds a message that can be sent to the class of the category target.
* @param testParameter A string argument.
* @returns An object.
*/
+ (NSObject *) testClassMethod:(NSObject *)testParameter;
@end