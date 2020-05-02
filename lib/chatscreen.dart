import 'package:flutter/material.dart';

class ChatScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        elevation: 1,
        title: Text(
          "ChatBot",
          style: TextStyle(letterSpacing: 0.5),
        ),
      ),
      body: MessageArea(),
    );
  }
}

class MessageArea extends StatefulWidget {
  MessageArea({Key key}) : super(key: key);

  @override
  _MessageAreaState createState() => _MessageAreaState();
}

class _MessageAreaState extends State<MessageArea> {
  TextEditingController _sendController;
  ScrollController _listScrollController;
  List<String> messageList = ["Hi! How are you", "I'm fine", "Thankyou"];
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        // mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: <Widget>[
          chatList(),
          sendArea(),
        ],
      ),
    );
  }
  @override
  void initState() { 
    super.initState();
    _listScrollController = new ScrollController(initialScrollOffset: 0,keepScrollOffset: false);
    _sendController = new TextEditingController();
  }
  Widget chatList() {
    return Expanded(
      child: ListView.builder(
          controller: _listScrollController,
          itemCount: messageList.length,
          itemBuilder: (context, index) {
            return Align(
              alignment: Alignment.centerRight,
              child: Container(
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Colors.grey[700]),
                padding: EdgeInsets.fromLTRB(10, 10, 40, 10),
                margin: EdgeInsets.fromLTRB(0, 15, 10, 0),
                child: Text(
                  messageList[index],
                  style: TextStyle(color: Colors.white, fontSize: 18),
                ),
              ),
            );
          }),
    );
  }

  Widget sendArea() {
    return Row(
      children: <Widget>[
        typeArea(),
        Container(
            margin: EdgeInsets.fromLTRB(0, 10, 10, 10),
            child: IconButton(
              onPressed: () {
                setState(() {
                  if (_sendController.value.text.isNotEmpty) {
                    messageList.add(_sendController.value.text);
                    _listScrollController.animateTo(
                        _listScrollController.position.maxScrollExtent,
                        duration: Duration(milliseconds: 500),
                        curve: Curves.easeIn);
                    _sendController.clear();
                  }
                });
              },
              icon: Icon(Icons.send),
              color: Colors.grey[700],
              iconSize: 40,
            ))
      ],
    );
  }

  Widget typeArea() {
    return Expanded(
      child: Container(
        height: 60,
        alignment: Alignment.center,
        margin: EdgeInsets.all(10),
        padding: EdgeInsets.fromLTRB(14, 10, 14, 10),
        decoration: BoxDecoration(
          color: Colors.grey[500],
          borderRadius: BorderRadius.all(Radius.circular(40)),
        ),
        child: TextField(
          controller: _sendController,
          decoration: InputDecoration(
            border: InputBorder.none,
            hintText: "Type message here",
            hintStyle: TextStyle(
                fontWeight: FontWeight.w400,
                color: Colors.white,
                letterSpacing: 1,
                fontSize: 17),
          ),
        ),
      ),
    );
  }
}
