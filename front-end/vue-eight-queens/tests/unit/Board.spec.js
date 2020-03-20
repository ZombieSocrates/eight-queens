import { shallowMount, mount } from '@vue/test-utils'
import Board from '@/components/Board'

describe('Board', () => {

  it('has the same number of rows as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 3
      }
    })
    const rowCount = testBoard.findAll('.row').length
    expect(rowCount).toEqual(testBoard.vm.dimension)

  })

  it('has the same number of columns as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 6
      }
    })
    const cellCount = testBoard.findAll({name: 'Cell'}).length
    const colCount = cellCount / testBoard.vm.dimension
    expect(colCount).toEqual(testBoard.vm.dimension)
  })

  it('has props.queensCount queens, if props.startState not given', () => {
    // must use mount here because I need the cell within the board ...
    const testBoard = mount(Board, {
      propsData: {
        dimension: 3,
        queensCount: 3
      }
    })
    const queensCount = testBoard.vm.queensCount
    let queenCellArray = testBoard
      .findAll({name: 'Cell'})
      .filter(w => w.vm.$data.hasQueen)
    expect(queenCellArray.length).toEqual(queensCount)
  })

  it('changes the position of queens when data.currentState changes', ()=> {
    const testBoard = mount(Board, {
      propsData: {
        dimension: 5,
        queensCount: 1, 
        startState: '55'
      }
    })
    const queensCountPrior = testBoard.vm.queensCount
    testBoard.setData({currentState:'11'})
    let cellArray = testBoard
      .findAll({name: 'Cell'})
    expect(cellArray.at(0).vm.$data.hasQueen).toBe(true)
    let queensCountAfter = cellArray
      .filter(w => w.vm.$data.hasQueen).length
    expect(queensCountPrior).toEqual(queensCountAfter)
  })

  it('errors when you put a queen in a cell that doesn\'t exist', () =>{
    expect(() => {
      let testBoard = shallowMount(Board, {
        propsData: {
          dimension: 8,
          queensCount: 1,
          startState: '11'
          }
      })
      testBoard.setData({currentState: '19'})
      return testBoard.vm.validBoardState
    }).toThrowError('Queen Out Of Range')
    expect(() => { shallowMount(Board, {
        propsData: {
          dimension: 8,
          queensCount: 1,
          startState: '08'
          }
      }).vm.validBoardState
    }).toThrowError('Queen Out Of Range')
  })

  it('errors when data.currentState doesn\'t specify proper number of queens', () =>{
    expect(() => { shallowMount(Board, {
        propsData: {
          dimension: 4,
          queensCount: 2,
          startState: '13'
          }
      }).vm.validBoardState
    }).toThrowError('Improper Number of Queens')
    expect(() => {
      let testBoard = shallowMount(Board, {
        propsData: {
          dimension: 8,
          queensCount: 3,
          startState: '118855'
          }
      })
      testBoard.setData({currentState: '11885577'})
      return testBoard.vm.validBoardState
    }).toThrowError('Improper Number of Queens')
  })

  it('errors when data.currentState includes duplicate positions', () => {
    expect(() => { shallowMount(Board, {
        propsData: {
          dimension: 5,
          queensCount: 3,
          startState: '123412'
          }
      }).vm.validBoardState
    }).toThrowError('Duplicate Queen Positions')
    expect(() => {
      let testBoard = shallowMount(Board, {
        propsData: {
          dimension: 7,
          queensCount: 3,
          startState: '112233'
          }
      })
      testBoard.setData({currentState: '223322'})
      return testBoard.vm.validBoardState
    }).toThrowError('Duplicate Queen Positions')
  })
})