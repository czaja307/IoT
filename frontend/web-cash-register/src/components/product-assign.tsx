"use client"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { editData, fetchData } from "@/lib/api";

import * as React from "react"

import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

// interface TerminalProps {
//   id: number;
//   name: string;
// }
export function SelectTerminal({terminals, terminal, setTerminal}: {terminals: string[], terminal: string, setTerminal: (value: string) => void}) {
  return (
    <Select
      onValueChange={(value: string) => setTerminal(value)}
      defaultValue={terminal}
    >
      <SelectTrigger>
        <SelectValue
          placeholder={terminal ? terminal : 'Wybierz terminal'}/>
      </SelectTrigger>
      <SelectContent>
        {terminals.map((item, index) => (
          <SelectItem value={item} key={index}>
            {item}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}



export function ProductAssign({productId} : { productId: number }) {
  const [terminal, setTerminal] = useState<string>("");

  const terminalsMutation = useMutation({
    mutationFn: (data: {terminal_id: number, product_id: number}) => {
      return editData("terminals/products", "PUT", { body: JSON.stringify(data) });
    },
    onSuccess: () => {
      alert(`Dodano powiązanie`);
    },
    onError: async (error: any) => {
      if (error) {
        alert(`Nie udało się powiązać`);
      }
    }
  });


  const { data: terminals, isLoading: isLoading, isError: isError } = useQuery({
    queryKey: ["terminals"],
    queryFn: fetchProducts
  });

  if (isLoading ||!terminals) {
    return (
      <div>loading...</div>

    );
  }
  if (isError) {
    return <div>error</div>;
  }

  const handleSubmit = () => {

    if (!terminal) {
      alert("All fields are required");
      return;
    }

    const payload = {
      terminal_id: Number(terminal),
      product_id: productId,
    };

    terminalsMutation.mutate(payload);
  };

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button >Przypisz</Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Proszę wybrać terminal</AlertDialogTitle>
          <AlertDialogDescription>
            <SelectTerminal terminals={terminals} terminal={terminal} setTerminal={setTerminal}/>
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Anuluj</AlertDialogCancel>
          <AlertDialogAction onClick={handleSubmit} type={"submit"}>Zatwierdż</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

const fetchProducts = async () => fetchData<string[]>("terminals/");