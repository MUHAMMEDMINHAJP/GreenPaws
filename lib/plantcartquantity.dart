//
// import 'package:flutter/material.dart';
// import 'package:fluttertoast/fluttertoast.dart';
// import 'package:greenpaws/user_home.dart';
// import 'package:greenpaws/view_shopproducts.dart';
//
// import 'package:http/http.dart' as http;
// import 'dart:convert';
// import 'package:shared_preferences/shared_preferences.dart';
// void main() {
//   runApp(const ViewReply());
// }
//
// class ViewReply extends StatelessWidget {
//   const ViewReply({super.key});
//
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'View Reply',
//       theme: ThemeData(
//
//         colorScheme: ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 18, 82, 98)),
//         useMaterial3: true,
//       ),
//       home: const plantcartquantity(title: 'View Reply'),
//     );
//   }
// }
//
// class plantcartquantity extends StatefulWidget {
//   const plantcartquantity({super.key, required this.title});
//
//   final String title;
//
//   @override
//   State<plantcartquantity> createState() => _plantcartquantityState();
// }
//
// class _plantcartquantityState extends State<plantcartquantity> {
//
//   _plantcartquantityState(){
//     viewreply();
//   }
//
//   List<String> id_= <String>[];
//   List<String> plant_id_= <String>[];
//   List<String> quantity_= <String>[];
//
//
//
//
//
//
//   Future<void> viewreply() async {
//     List<String> id = <String>[];
//     List<String> shop_name= <String>[];
//     List<String> owner_name= <String>[];
//     List<String> email= <String>[];
//     List<String> place= <String>[];
//     List<String> post= <String>[];
//     List<String> pin= <String>[];
//     List<String> district= <String>[];
//     List<String> photo= <String>[];
//     List<String> licence= <String>[];
//     List<String> ph_no= <String>[];
//
//     try {
//       SharedPreferences sh = await SharedPreferences.getInstance();
//       String urls = sh.getString('url').toString();
//       String lid = sh.getString('lid').toString();
//       String url = '$urls/myapp/user_viewshops/';
//
//       var data = await http.post(Uri.parse(url), body: {
//
//         'lid':lid
//
//       });
//       var jsondata = json.decode(data.body);
//       String statuss = jsondata['status'];
//
//       var arr = jsondata["data"];
//
//       print(arr.length);
//
//       for (int i = 0; i < arr.length; i++) {
//         id.add(arr[i]['id'].toString());
//         shop_name.add(arr[i]['shop_name']);
//         owner_name.add(arr[i]['owner_name']);
//         email.add(arr[i]['email']);
//         place.add(arr[i]['place']);
//         post.add(arr[i]['post'].toString());
//         pin.add(arr[i]['pin'].toString());
//         district.add(arr[i]['district']);
//         photo.add(urls+arr[i]['photo']);
//         licence.add(arr[i]['licence']);
//         ph_no.add(arr[i]['ph_no'].toString());
//       }
//
//       setState(() {
//         id_ = id;
//         shop_name_ = shop_name;
//         owner_name_ = owner_name;
//         email_ = email;
//         place_ = place;
//         post_ = post;
//         pin_ = pin;
//         district_= district;
//         photo_ = photo;
//         licence_=licence;
//         ph_no_=ph_no;
//       });
//
//       print(statuss);
//     } catch (e) {
//       print("Error ------------------- " + e.toString());
//       //there is error during converting file image to base64 encoding.
//     }
//   }
//
//
//
//
//   @override
//   Widget build(BuildContext context) {
//
//
//
//     return WillPopScope(
//       onWillPop: () async{ return true; },
//       child: Scaffold(
//         appBar: AppBar(
//           leading: BackButton( onPressed:() {
//
//             Navigator.push(
//               context,
//               MaterialPageRoute(builder: (context) => UserHome(title: '',)),);
//           },),
//           backgroundColor: Theme.of(context).colorScheme.primary,
//           title: Text('PLANT SHOPS'),
//         ),
//         body: ListView.builder(
//           physics: BouncingScrollPhysics(),
//           // padding: EdgeInsets.all(5.0),
//           // shrinkWrap: true,
//           itemCount: id_.length,
//           itemBuilder: (BuildContext context, int index) {
//             return ListTile(
//               onLongPress: () {
//                 print("long press" + index.toString());
//               },
//               title: Padding(
//                   padding: const EdgeInsets.all(8.0),
//                   child: Column(
//                     children: [
//                       Card(
//                         child:
//                         Row(
//                             children: [
//                               Column(
//                                 children: [
//
//                                   CircleAvatar(
//                                     backgroundImage: NetworkImage(photo_[index]),
//                                     radius: 50,
//                                   ),
//                                   Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(shop_name_[index]),
//                                   ),
//                                   Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(owner_name_[index]),
//                                   ),    Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(email_[index]),
//                                   ),  Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(ph_no_[index]),
//                                   ),     Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(place_[index]),
//                                   ),     Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(post_[index]),
//                                   ),     Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(pin_[index]),
//                                   ),    Padding(
//                                     padding: EdgeInsets.all(5),
//                                     child: Text(district_[index]),
//                                   ),
//                                   Padding(
//                                       padding: EdgeInsets.all(5),
//                                       child:   ElevatedButton(onPressed: () async {
//                                         SharedPreferences  sh= await SharedPreferences.getInstance();
//                                         sh.setString('sid',id_[index]);
//                                         // senddata();
//                                         Navigator.push(context, MaterialPageRoute(builder: (context)=>viewshopproducts(title: ''),));
//
//                                       }, child: Text('View Products'))
//                                   ),
//
//                                 ],
//                               ),
//
//                             ]
//                         ),
//
//                         elevation: 8,
//                         margin: EdgeInsets.all(10),
//                       ),
//                     ],
//                   )),
//             );
//           },
//         ),
//
//       ),
//     );
//   }
// }
