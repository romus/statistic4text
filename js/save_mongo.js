/**
 * User: romus
 * Date: 20.08.13
 * Time: 20:05
 */

conn = new Mongo();
db = conn.getDB("statistic");
db.addUser({user:"statistic", pwd:"statistic", roles:["readWrite"]});
