//! \brief demonstrates member groups
class GroupedMembers {

public:

    ///@{   @name myGroup
    void in_mygroup_one(int myParameter);  ///< A function
    void in_mygroup_two(int myParameter);  ///< Another function
    ///@}

    void not_in_mygroup(int myParameter);  ///< This one is not in myGroup

};
