
/*! \brief A failing class
 *  \class Failing */
class Failing {
public:
    /**
     * @name Some section .
     * THIS IS CAUSING THE ERROR, must have an empty star line above
     *
     * @{
     */
    int getSomething() const; ///< some docs
    bool isSomething() const; ///< some more docs
    //@}
};

