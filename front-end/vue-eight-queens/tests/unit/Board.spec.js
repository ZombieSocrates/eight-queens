import { shallowMount, mount } from '@vue/test-utils'
import Board from '@/components/Board'

describe('Board', () => {

  it('has the same number of rows as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 3
      }
    })
    // console.log(`Dimension is ${testBoard.vm.dimension}`)
    const rowCount = testBoard.findAll('.row').length
    // console.log(`Row count is ${rowCount}`)
    expect(rowCount).toEqual(testBoard.vm.dimension)

  })

  it('has the same number of columns as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 6
      }
    })
    // console.log(`Dimension is ${testBoard.vm.dimension}`)
    const cellCount = testBoard.findAll({name: 'Cell'}).length
    const colCount = cellCount / testBoard.vm.dimension
    // console.log(`Column count is ${colCount}`)
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
    // console.log(`Queens on the board: ${queensCount}`)
    // console.log(`prop.StartState: ${testBoard.vm.startState}`)
    // console.log(`Randomly generated state: ${testBoard.vm.currentState}`)
    // console.log(testBoard.vm.queenLocations)
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
    console.log(`Queens on the board: ${queensCountPrior}`)
    console.log(`State Before: ${testBoard.vm.currentState}`)
    testBoard.setData({currentState:'11'})
    console.log(`State After: ${testBoard.vm.currentState}`)
    let cellArray = testBoard
      .findAll({name: 'Cell'})
    expect(cellArray.at(0).vm.$data.hasQueen).toBe(true)
    let queensCountAfter = cellArray
      .filter(w => w.vm.$data.hasQueen).length
    expect(queensCountPrior).toEqual(queensCountAfter)
  })
})