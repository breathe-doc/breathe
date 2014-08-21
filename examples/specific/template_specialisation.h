
/*!
A generic template class.
*/
template<typename T>
class TemplateClass
{
};

/*! 
A partial specialization of TemplateClass for pointer types.
*/
template<typename T>
class TemplateClass<T*>
{
};

