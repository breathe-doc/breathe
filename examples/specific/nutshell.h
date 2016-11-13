/**
    \file nutshell.h
    An overly extended example of how to use breathe
*/

/*!
    With a little bit of a elaboration, should you feel it necessary.
*/
class Nutshell
{
public:

    //! Our tool set
    /*! The various tools we can opt to use to crack this particular nut */
    enum Tool
    {
        kHammer = 0,          //!< What? It does the job
        kNutCrackers,         //!< Boring
        kNinjaThrowingStars   //!< Stealthy
    };

    //! Nutshell constructor
    Nutshell();

    //! Nutshell destructor
    ~Nutshell();

    /*! Crack that shell with specified tool

      \param tool the tool with which to crack the nut
    */
    void crack( Tool tool );

    /*!
      \return Whether or not the nut is cracked
    */
    bool isCracked();

private:

    //! Our cracked state
    bool m_isCracked;

};


