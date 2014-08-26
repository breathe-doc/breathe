#ifndef QT_OBJECT_H
#define QT_OBJECT_H

#include

class QtSlotExample: public QObject
{
    Q_OBJECT

    public:

    /*!
     *\param iShownParameter
     This is shown in declaration
     */
    void workingFunction( int iShownParameter ) { Q_UNUSED( iShownParameter ; ) }

    public slots:

    /*!
     *\param iShown
     This is in function declaration
     */
    void workingSlot( int iShown ) { iShown; }
};

#endif
