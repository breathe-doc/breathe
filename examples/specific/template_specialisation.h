
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

/*!
A generic template class.
*/
template<typename T>
class SecondTemplateClass
{
};

/*!
A partial specialization of SecondTemplateClass for pointer types.
*/
template<typename T>
class SecondTemplateClass<T*>
{
};
