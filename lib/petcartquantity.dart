
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:greenpaws/%60viewsinglepet.dart';
import 'package:greenpaws/user_home.dart';
import 'package:greenpaws/viewpetshops.dart';
import 'package:greenpaws/viewsingleplant.dart';

import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
void main() {
  runApp(const ViewReply());
}

class ViewReply extends StatelessWidget {
  const ViewReply({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'View Reply',
      theme: ThemeData(

        colorScheme: ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 18, 82, 98)),
        useMaterial3: true,
      ),
      home: const petcartview(title: 'View Reply'),
    );
  }
}

class petcartview extends StatefulWidget {
  const petcartview({super.key, required this.title});

  final String title;

  @override
  State<petcartview> createState() => _petcartviewState();
}

class _petcartviewState extends State<petcartview> {

  _petcartviewState(){
    viewreply();
  }

  List<String> id_= <String>[];
  List<String> pet_name_= <String>[];
  List<String> breed_name_= <String>[];
  List<String> photo_= <String>[];
  List<String> age_= <String>[];
  List<String> price_= <String>[];
  List<String> details_= <String>[];





  Future<void> viewreply() async {
    List<String> id = <String>[];
    List<String> pet_name= <String>[];
    List<String> breed_name= <String>[];
    List<String> photo= <String>[];
    List<String> age= <String>[];
    List<String> price= <String>[];
    List<String> details= <String>[];

    try {
      SharedPreferences sh = await SharedPreferences.getInstance();
      String urls = sh.getString('url').toString();
      String lid = sh.getString('lid').toString();
      String sid= sh.getString('psid').toString();
      String url = '$urls/myapp/user_viewshoppet/';

      var data = await http.post(Uri.parse(url), body: {

        'lid':lid,
        'sid':sid


      });
      var jsondata = json.decode(data.body);
      String statuss = jsondata['status'];

      var arr = jsondata["data"];

      print(arr.length);

      for (int i = 0; i < arr.length; i++) {
        id.add(arr[i]['id'].toString());
        pet_name.add(arr[i]['pet_name'].toString());
        breed_name.add(arr[i][' breed_name'].toString());
        age.add(arr[i]['age'].toString());
        photo.add(urls+arr[i]['photo'].toString());
        price.add(arr[i]['price'].toString());
        details.add(arr[i]['details'].toString());
      }

      setState(() {
        id_ = id;
        pet_name_= pet_name;
        breed_name_= breed_name;
        age_= age;
        photo_ = photo;
        price_=price;
        details_=details;
      });

      print(statuss);
    } catch (e) {
      print("Error ------------------- " + e.toString());
      //there is error during converting file image to base64 encoding.
    }
  }




  @override
  Widget build(BuildContext context) {



    return WillPopScope(
      onWillPop: () async{ return true; },
      child: Scaffold(
        appBar: AppBar(
          leading: BackButton( onPressed:() {

            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => viewpetshops(title: '',)),);

          },),
          backgroundColor: Theme.of(context).colorScheme.primary,
          title: Text(widget.title),
        ),
        body: ListView.builder(
          physics: BouncingScrollPhysics(),
          // padding: EdgeInsets.all(5.0),
          // shrinkWrap: true,
          itemCount: id_.length,
          itemBuilder: (BuildContext context, int index) {
            return ListTile(
              onLongPress: () {
                print("long press" + index.toString());
              },
              title: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Column(
                    children: [
                      Card(
                        child:
                        Row(
                            children: [
                              Column(
                                children: [

                                  CircleAvatar(
                                    backgroundImage: NetworkImage(photo_[index]),
                                    radius: 50,
                                  ),
                                  Padding(
                                    padding: EdgeInsets.all(5),
                                    child: Text(pet_name_[index]),
                                  ),
                                  // Padding(
                                  //   padding: EdgeInsets.all(5),
                                  //   child: Text(scientific_name_[index]),
                                  // ),    Padding(
                                  //   padding: EdgeInsets.all(5),
                                  //   child: Text(size_[index]),
                                  // ),
                              Padding(
                                    padding: EdgeInsets.all(5),
                                    child: Text(price_[index]),
                                  ),
                      // Padding(
                                  //   padding: EdgeInsets.all(5),
                                  //   child: Text(details_[index]),
                                  // ),
                                  Padding(
                                      padding: EdgeInsets.all(5),
                                      child:   ElevatedButton(onPressed: () async {
                                        SharedPreferences  sh= await SharedPreferences.getInstance();
                                        sh.setString('pid',id_[index]);
                                        // senddata();
                                        Navigator.push(context, MaterialPageRoute(builder: (context)=>viewsinglepet(title: ''),));

                                      }, child: Text('View Pet'))
                                  ),
                                ],
                              ),

                            ]
                        ),

                        elevation: 8,
                        margin: EdgeInsets.all(10),
                      ),
                    ],
                  )),
            );
          },
        ),

      ),
    );
  }
}
