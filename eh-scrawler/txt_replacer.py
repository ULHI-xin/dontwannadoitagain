#!/usr/bin/env python
# coding: utf-8

import argparse


def read_file(filepath):
    with open(filepath, 'r') as fr:
        lines = [l for l in fr.readlines()]
    return lines


def replace_outside_brackets(lines, src, tgt, bracket_start, bracket_end):
    result_lines = []

    _in_bracket = False
    for l in lines:
        _result_l = ""
        for c in l:

            if c in bracket_start:
                _in_bracket = True
            elif c in bracket_end:
                _in_bracket = False

            if _in_bracket:
                _result_l += c
            else:
                _result_l += c if c != src else tgt
        # print(_result_l, type(_result_l))
        result_lines.append(_result_l)

    return result_lines


def main(file_in, src, tgt, bracket_start, bracket_end):
    lines = read_file(file_in)
    ext = file_in[file_in.rfind('.'):]
    print(ext)
    lines_replaced = replace_outside_brackets(lines, src, tgt, bracket_start, bracket_end)

    file_out = file_in.replace(ext, f".{src}_2_{tgt}{ext}")
    with open(file_out, 'w') as fw:
        for l in lines_replaced:
            fw.write(l)
    print(file_out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_in")
    parser.add_argument("src_word")
    parser.add_argument("tgt_word")
    parser.add_argument("bracket_start")
    parser.add_argument("bracket_end")
    args = parser.parse_args()
    print(args)

    main(args.file_in, args.src_word, args.tgt_word, args.bracket_start, args.bracket_end)
