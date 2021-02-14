/**
 * \brief This is a simple Markdown table example.
 *
 * Following is a simple table using Markdown syntax.
 *
 * First Header  | Second Header
 * ------------- | -------------
 * Content Cell  | Content Cell
 * Content Cell  | Content Cell
 *
 * And this is some more text.
 */
class Table_1
{
};

/**
 * \brief This is a Markdown table with alignment.
 *
 * Following is a table with alignment using Markdown syntax.
 *
 * | Right | Center | Left  |
 * | ----: | :----: | :---- |
 * | 10    | 10     | 10    |
 * | 1000  | 1000   | 1000  |
 *
 * And this is some more text.
 */
class Table_2
{
};

/**
 * \brief This is a Markdown table with rowspan and alignment.
 *
 * Following is a table with rowspan and alignment using Markdown syntax.
 *
 * | Right | Center | Left  |
 * | ----: | :----: | :---- |
 * | 10    | 10     | 10    |
 * | ^     | 1000   | 1000  |
 *
 * And this is some more text.
 */
class Table_3
{
};

/**
 * \brief This is a Markdown table with colspan and alignment.
 *
 * Following is a table with colspan and alignment using Markdown syntax.
 *
 * | Right | Center | Left  |
 * | ----: | :----: | :---- |
 * | 10    | 10     | 10    |
 * | 1000  |||
 *
 * And this is some more text.
 */
class Table_4
{
};

/**
 * \brief This is a Doxygen table.
 *
 * Following is a table using Doxygen syntax (and all supported features).
 *
 * <table>
 * <caption id="multi_row">Complex table</caption>
 * <tr><th>Column 1                      <th>Column 2        <th>Column 3
 * <tr><td rowspan="2">cell row=1+2,col=1<td>cell row=1,col=2<td>cell row=1,col=3
 * <tr><td rowspan="2">cell row=2+3,col=2                    <td>cell row=2,col=3
 * <tr><td>cell row=3,col=1                                  <td rowspan="2">cell row=3+4,col=3
 * <tr><td colspan="2">cell row=4,col=1+2
 * <tr><td>cell row=5,col=1              <td colspan="2">cell row=5,col=2+3
 * <tr><td colspan="2" rowspan="2">cell row=6+7,col=1+2      <td>cell row=6,col=3
 * <tr>                                                      <td>cell row=7,col=3
 * <tr><td>cell row=8,col=1              <td>cell row=8,col=2\n
 *   <table>
 *     <tr><td>Inner cell row=1,col=1<td>Inner cell row=1,col=2
 *     <tr><td>Inner cell row=2,col=1<td>Inner cell row=2,col=2
 *   </table>
 *   <td>cell row=8,col=3
 *   <ul>
 *     <li>Item 1
 *     <li>Item 2
 *   </ul>
 * </table>
 *
 * And this is some more text.
 */
class Table_5
{
};
