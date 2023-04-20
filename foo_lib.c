/*******************************************************************
 * foo_lib.c
 * Compiladores 20231
 * Ingenieria de Sistemas y Computacion - UTP
 *
 * Contiene funciones/variables libreria externa para foo.c
 *******************************************************************
*/

// Prueba varible global.
float stuff_count;

/* 
    Prueba de definicióíííýýý´t´´f´reé´´f´d´w´´fé´w´´x´´s´}a]A`sn de funcion estatica, se asegura
    de que no entre en conflicto con fib() definido en foo.c.  
*/
static int fib() {
  return stuff_count += 1;
}

// Incremento variable global.
int increment_stuff_count() {
  fib();
  return 0;
}
