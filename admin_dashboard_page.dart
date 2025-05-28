import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AdminDashboardPage extends StatefulWidget {
  final String nomeFuncionario;

  const AdminDashboardPage({super.key, required this.nomeFuncionario});

  @override
  State<AdminDashboardPage> createState() => _AdminDashboardPageState();
}

class _AdminDashboardPageState extends State<AdminDashboardPage> {
  List<Map<String, dynamic>> connectionRequests = [];
  List<Map<String, dynamic>> connectedComputers = [];

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    await fetchConnectionRequests();
    await fetchConnectedComputers();
  }

  Future<void> fetchConnectionRequests() async {
    final url = Uri.parse('http://127.0.0.1:5000/agente/requests');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      setState(() {
        connectionRequests = List<Map<String, dynamic>>.from(jsonDecode(response.body));
      });
    }
  }

  Future<void> fetchConnectedComputers() async {
    final url = Uri.parse('http://127.0.0.1:5000/agente/computers');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      setState(() {
        connectedComputers = List<Map<String, dynamic>>.from(jsonDecode(response.body));
      });
    }
  }

  Future<void> acceptConnection(int idComp) async {
    final url = Uri.parse('http://127.0.0.1:5000/agente/accept/$idComp');
    final response = await http.post(url);

    if (response.statusCode == 200) {
      await fetchData();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Conexão aceita')),
      );
    }
  }

  Future<void> disconnectComputer(int idComp) async {
    final url = Uri.parse('http://127.0.0.1:5000/agente/disconnect/$idComp');
    final response = await http.post(url);

    if (response.statusCode == 200) {
      await fetchData();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Computador desconectado')),
      );
    }
  }

  void _realizarLogout(BuildContext context) {
    Navigator.pop(context);
  }

  void _registrarParalisacao(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Paralisação registrada')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Bem-vindo, ${widget.nomeFuncionario}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: fetchData,
          )
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text('🔌 Requisições de Conexão', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          ...connectionRequests.map((comp) => Card(
            child: ListTile(
              title: Text('ID: ${comp['id_comp']} - ${comp['marca']} (${comp['so']})'),
              subtitle: Text('Cor: ${comp['cor']}'),
              trailing: ElevatedButton(
                onPressed: () => acceptConnection(comp['id_comp']),
                child: const Text('Aceitar'),
            ),
            ),
          )),
          const SizedBox(height: 30),
          const Text('🟢 Computadores Conectados', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          ...connectedComputers.map((comp) => Card(
            child: ListTile(
              title: Text('ID: ${comp['id_comp']} - ${comp['marca']} (${comp['so']})'),
              subtitle: Text('IP: ${comp['ip']}'),
              trailing: ElevatedButton(
                onPressed: () => disconnectComputer(comp['id_comp']),
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                child: const Text('Desconectar'),
              ),
            ),
          )),
          const SizedBox(height: 30),
          ElevatedButton.icon(
            icon: const Icon(Icons.logout),
            label: const Text('Encerrar Turno (Logout)'),
            onPressed: () => _realizarLogout(context),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
          ),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            icon: const Icon(Icons.pause_circle),
            label: const Text('Registrar Paralisação'),
            onPressed: () => _registrarParalisacao(context),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.orangeAccent),
          ),
        ],
      ),
    );
  }
}
