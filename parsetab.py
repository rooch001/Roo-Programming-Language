
# parsetab.py

# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'nonassocPRINTleftPLUSMINUSleftTIMESDIVnonassocUMINUSASSIGN DIV ID LPAREN MINUS NUMBER PLUS PRINT RPAREN TIMESexpr : ID ASSIGN exprexpr : IDexpr : PRINT exprexpr : expr : expr PLUS exprexpr : expr MINUS exprexpr : MINUS expr %prec UMINUSexpr : expr TIMES expr\n                | expr DIV exprexpr : NUMBERexpr : LPAREN expr RPAREN'
    
_lr_action_items = {'ID':([0,3,4,6,7,8,9,10,11,],[2,2,2,2,2,2,2,2,2,]),'PRINT':([0,3,4,6,7,8,9,10,11,],[3,3,3,3,3,3,3,3,3,]),'PLUS':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,],[-4,7,-2,-4,-4,-10,-4,-4,-4,-4,-4,-4,7,-7,7,-5,-6,-8,-9,7,-11,]),'MINUS':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,],[4,8,-2,4,4,-10,4,4,4,4,4,4,8,-7,8,-5,-6,-8,-9,8,-11,]),'TIMES':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,],[-4,9,-2,-4,-4,-10,-4,-4,-4,-4,-4,-4,9,-7,9,9,9,-8,-9,9,-11,]),'DIV':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,],[-4,10,-2,-4,-4,-10,-4,-4,-4,-4,-4,-4,10,-7,10,10,10,-8,-9,10,-11,]),'$end':([0,1,2,3,4,5,7,8,9,10,11,12,13,15,16,17,18,19,20,],[-4,0,-2,-4,-4,-10,-4,-4,-4,-4,-4,-3,-7,-5,-6,-8,-9,-1,-11,]),'NUMBER':([0,3,4,6,7,8,9,10,11,],[5,5,5,5,5,5,5,5,5,]),'LPAREN':([0,3,4,6,7,8,9,10,11,],[6,6,6,6,6,6,6,6,6,]),'ASSIGN':([2,],[11,]),'RPAREN':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,],[-2,-4,-4,-10,-4,-4,-4,-4,-4,-4,-3,-7,20,-5,-6,-8,-9,-1,-11,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expr':([0,3,4,6,7,8,9,10,11,],[1,12,13,14,15,16,17,18,19,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expr","S'",1,None,None,None),
  ('expr -> ID ASSIGN expr','expr',3,'p_id_statement','new.py',70),
  ('expr -> ID','expr',1,'p_id','new.py',74),
  ('expr -> PRINT expr','expr',2,'p_print_statement','new.py',78),
  ('expr -> <empty>','expr',0,'p_empty','new.py',82),
  ('expr -> expr PLUS expr','expr',3,'p_add','new.py',86),
  ('expr -> expr MINUS expr','expr',3,'p_sub','new.py',90),
  ('expr -> MINUS expr','expr',2,'p_expr2uminus','new.py',94),
  ('expr -> expr TIMES expr','expr',3,'p_mult_div','new.py',98),
  ('expr -> expr DIV expr','expr',3,'p_mult_div','new.py',99),
  ('expr -> NUMBER','expr',1,'p_expr2NUM','new.py',110),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_parens','new.py',114),
]
