
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:greenpaws/user_home.dart';

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
      home: const viewplants(title: 'View Reply'),
    );
  }
}

class viewplants extends StatefulWidget {
  const viewplants({super.key, required this.title});

  final String title;

  @override
  State<viewplants> createState() => _viewplantsState();
}

class _viewplantsState extends State<viewplants> {

  _viewplantsState(){
    viewreply();
  }

  List<String> id_= <String>[];
  List<String> plant_name_= <String>[];
  List<String> scientific_name_= <String>[];
  List<String> size_= <String>[];
  List<String> plant_type_= <String>[];
  List<String> photo_= <String>[];
  List<String> price_= <String>[];
  List<String> details_= <String>[];





  Future<void> viewreply() async {
    List<String> id = <String>[];
    List<String> plant_name= <String>[];
    List<String> scientific_name= <String>[];
    List<String> size= <String>[];
    List<String> plant_type= <String>[];
    List<String> photo= <String>[];
    List<String> price= <String>[];
    List<String> details= <String>[];

    try {
      SharedPreferences sh = await SharedPreferences.getInstance();
      String urls = sh.getString('url').toString();
      String lid = sh.getString('lid').toString();
      String url = '$urls/myapp/user_viewplant/';

      var data = await http.post(Uri.parse(url), body: {

        'lid':lid

      });
      var jsondata = json.decode(data.body);
      String statuss = jsondata['status'];

      var arr = jsondata["data"];

      print(arr.length);

      for (int i = 0; i < arr.length; i++) {
        id.add(arr[i]['id'].toString());
        plant_name.add(arr[i]['plant_name']);
        scientific_name.add(arr[i][' scientific_name']);
        size.add(arr[i]['size'].toString());
        plant_type.add(arr[i]['plant_type']);
        photo.add(urls+arr[i]['photo']);
        price.add(arr[i]['price'].toString());
        details.add(arr[i]['details']);
      }

      setState(() {
        id_ = id;
        plant_name_= plant_name;
        scientific_name_= scientific_name;
        size_= size;
        plant_type_= plant_type;
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
              MaterialPageRoute(builder: (context) => UserHome(title: '',)),);

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
                                    child: Text(plant_name_[index]),
                                  ),
                                  Padding(
                                    padding: EdgeInsets.all(5),
                                    child: Text(scientific_name_[index]),
                                  ),    Padding(
                                    padding: EdgeInsets.all(5),
                                    child: Text(size_[index]),
                                  ),  Padding(
                                    padding: EdgeInsets.all(5),
                                    child: Text(plant_type_[index]),
                                  ),     Padding(
                                    padding: EdgeInsets.all(5),
                                    child: Text(details_[index]),
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
