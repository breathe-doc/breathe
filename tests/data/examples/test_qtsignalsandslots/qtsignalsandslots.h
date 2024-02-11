#ifndef QT_OBJECT_H
#define QT_OBJECT_H

/*!
*\brief Forward declaration of QT API class

QT slots and signals typically `#include <QObject>`, but this example is parsed without QT SDK installed.
*/
extern class QObject;

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
     \param iShown
     This is in function declaration
     */
    void workingSignal( int iShown );

    public slots:

    /*!
     \param iShown
     This is in function declaration
     */
    void workingSlot( int iShown ) { iShown; }
};

#endif
