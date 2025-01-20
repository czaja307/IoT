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
import { useQuery } from "@tanstack/react-query";
import { fetchData } from "@/lib/api";
import { ProductProps } from "@/lib/types";

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface TerminalProps {
  id: number;
  name: string;
}
export function SelectTerminal({terminals, terminal, setTerminal}: {terminals: TerminalProps[], terminal: string, setTerminal: (value: string) => void}) {
  return (
    <Select
      onValueChange={(value: string) => setTerminal(value)}
      defaultValue={terminal}
    >
      <SelectTrigger>
        <SelectValue
          placeholder={terminal ? (terminals.find((item) => item.id.toString() === terminal)?.name) : 'Wybierz terminal'}/>
      </SelectTrigger>
      <SelectContent>
        {terminals.map((item, index) => (
          <SelectItem value={item.id.toString()} key={index}>
            {item.name}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}



export function ProductAssign({productId} : { productId: number }) {
  const [terminal, setTerminal] = useState<string>("");

  const { data: products, isLoading: isLoadingProducts, isError: isErrorProducts } = useQuery({
    queryKey: ["products"],
    queryFn: fetchProducts
  });

  if (isLoadingProducts || !products) {
    return (
      <div>loading...</div>

    );
  }
  if (isErrorProducts) {
    return <div>error</div>;
  }

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button >Przypisz</Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Proszę wybrać terminal</AlertDialogTitle>
          <AlertDialogDescription>
            <SelectTerminal terminals={products} terminal={terminal} setTerminal={setTerminal}/>
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Anuluj</AlertDialogCancel>
          <AlertDialogAction>Zatwierdż</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

const fetchProducts = async () => fetchData<ProductProps[]>("products");