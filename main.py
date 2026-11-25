import flet as ft
import json
import os

ARQUIVO = "livros.json"


def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar(lista):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def main(page: ft.Page):
    page.title = "Cadastro de Livros"

    livros = carregar()
    indice_edicao = [None]  # guarda a posição do livro que está sendo editado

    titulo = ft.TextField(label="Título")
    autor = ft.TextField(label="Autor")
    lista = ft.Column()
    botao = ft.Button("Adicionar")

    def mostrar():
        lista.controls.clear()
        for i in range(len(livros)):
            livro = livros[i]
            linha = ft.Row([
                ft.Text(livro["titulo"] + " - " + livro["autor"]),
                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, i=i: editar(i)),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, i=i: excluir(i)),
            ])
            lista.controls.append(linha)
        page.update()

    def gravar(e):
        if titulo.value == "" or autor.value == "":
            return
        livro = {"titulo": titulo.value, "autor": autor.value}
        if indice_edicao[0] is None:
            livros.append(livro)
        else:
            livros[indice_edicao[0]] = livro
            indice_edicao[0] = None
            botao.content = "Adicionar"
        salvar(livros)
        titulo.value = ""
        autor.value = ""
        mostrar()

    def editar(i):
        titulo.value = livros[i]["titulo"]
        autor.value = livros[i]["autor"]
        indice_edicao[0] = i
        botao.content = "Salvar"
        page.update()

    def excluir(i):
        livros.pop(i)
        salvar(livros)
        mostrar()

    botao.on_click = gravar

    page.add(titulo, autor, botao, lista)
    mostrar()


ft.run(main)
