#ifndef QT_OBJECT_H
#define QT_OBJECT_H

#include

class QtSignalSlotExample: public QObject
{
    Q_OBJECT

    public:

    /*!
     *\param iShownParameter
     This is shown in declaration
     */
    void workingFunction( int iShownParameter ) { Q_UNUSED( iShownParameter ; ) }

    signals:

    /*!
     *\param iShown
     This is in function declaration
     */
    void workingSignal( int iShown );

    public slots:

    /*!
     *\param iShown
     This is in function declaration
     */
    void workingSlot( int iShown ) { iShown; }
};

#endif
